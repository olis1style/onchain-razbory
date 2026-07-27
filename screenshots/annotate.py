#!/usr/bin/env python3
"""Разметка скриншотов Arkham: рамки, номера, подпись-легенда снизу."""
from PIL import Image, ImageDraw, ImageFont

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG  = "/System/Library/Fonts/Supplemental/Arial.ttf"
YEL, RED, GRN, BLU = "#ffc85c", "#ff5c7a", "#3ddc97", "#5b9dff"
BG, DIM, TXT = "#0a0c14", "#8b96b0", "#e8edf7"


def annotate(src, dst, boxes, crop_bottom=766):
    im = Image.open(src).convert("RGB").crop((0, 44, 1522, crop_bottom))
    W, H = im.size
    pad = 34 + 30 * len(boxes)
    out = Image.new("RGB", (W, H + pad), BG)
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    fb, fr = ImageFont.truetype(BOLD, 17), ImageFont.truetype(REG, 17)
    fnum = ImageFont.truetype(BOLD, 15)

    for i, (x1, y1, x2, y2, color, text) in enumerate(boxes, 1):
        y1, y2 = y1 - 44, y2 - 44
        d.rounded_rectangle([x1, y1, x2, y2], radius=6, outline=color, width=3)
        # номерной бейдж слева от рамки
        cx, cy = (x1 - 15) if x1 > 34 else (x1 + 17), y1 + (y2 - y1) // 2
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=color)
        w = d.textlength(str(i), font=fnum)
        d.text((cx - w / 2, cy - 9), str(i), font=fnum, fill=BG)
        # строка легенды
        ly = H + 22 + 30 * (i - 1)
        d.ellipse([16, ly, 44, ly + 28], fill=color)
        w = d.textlength(str(i), font=fnum)
        d.text((30 - w / 2, ly + 5), str(i), font=fnum, fill=BG)
        d.text((56, ly + 4), text, font=fr, fill=TXT)

    d.line([0, H, W, H], fill="#242c44", width=2)
    out.save(dst, quality=95)
    print(dst, out.size)


annotate("raw-hub.png", "gonka-arkham-hub.png", [
    (104, 66, 296, 92, YEL, "Метка Arkham «Jocy Lin (IOSG Ventures)?» — со знаком вопроса: это догадка нейросети, а не факт"),
    (778, 622, 1504, 652, GRN, "24 июля: $30 000 ушли покупателю «cryptochaoswar» — тому, кто скупал WGNK"),
    (778, 660, 1504, 690, RED, "16 июля: $500 000 отправлены на отдельный адрес, где лежат до сих пор"),
    (778, 698, 1504, 726, BLU, "Перед этим — тестовый перевод на $100, чтобы убедиться, что адрес рабочий"),
    (778, 734, 1504, 762, DIM, "Сами деньги пришли с горячего кошелька Binance — это ввод средств, а не покупка биржей"),
])

annotate("raw-cash.png", "gonka-arkham-cash.png", [
    (100, 104, 262, 136, RED, "$500 630 на балансе — и ни одной покупки с 16 июля"),
    (18, 244, 748, 280, YEL, "Вся сумма лежит в USDT: 500 473 монеты, готовые к сделке в любой момент"),
    (778, 622, 1504, 690, GRN, "Оба входящих перевода — с того же раздающего кошелька: сначала $100, потом $500 000"),
])

annotate("raw-buyer.png", "gonka-arkham-buyer.png", [
    (104, 66, 392, 92, YEL, "Кошелёк подписан ником с OpenSea — «cryptochaoswar». Других имён у него нет"),
    (18, 244, 748, 280, GRN, "651 377 WGNK на $125 тысяч — это 10,95% всего выпуска токена"),
    (18, 282, 748, 318, BLU, "Рядом позиция в MOR (Morpheus AI) — вторая ставка в том же секторе «крипта + ИИ»"),
    (778, 622, 1504, 652, RED, "Покупка тремя часами ранее: 90 760 WGNK получено прямо из пула Uniswap"),
])
