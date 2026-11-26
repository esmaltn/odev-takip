"""Komut satırı arayüzü: python -m odev_takip <komut> ..."""

import argparse
import sys

from odev_takip import depo
from odev_takip.odev import OdevHatasi, odev_metni, odev_olustur


def _ekle(args, yol):
    odevler = depo.yukle(yol)
    odev = odev_olustur(odevler, args.ders, args.baslik, args.teslim)
    odevler.append(odev)
    depo.kaydet(yol, odevler)
    print(f"Eklendi: {odev_metni(odev)}")


def parser_olustur():
    dosya_yardimi = (
        f"ödevlerin saklandığı JSON dosyası (varsayılan: {depo.ORTAM_DEGISKENI} "
        f"ortam değişkeni ya da {depo.VARSAYILAN_DOSYA})"
    )
    ortak = argparse.ArgumentParser(add_help=False)
    ortak.add_argument("--dosya", default=argparse.SUPPRESS, help=dosya_yardimi)

    parser = argparse.ArgumentParser(
        prog="python -m odev_takip",
        description="Ödev Takipçisi: derslerinin ödevlerini ve teslim tarihlerini takip et.",
    )
    parser.add_argument("--dosya", default=None, help=dosya_yardimi)
    alt = parser.add_subparsers(dest="komut", metavar="KOMUT")
    alt.required = True

    ekle = alt.add_parser("ekle", parents=[ortak], help="yeni ödev ekle")
    ekle.add_argument("--ders", required=True, help="dersin adı")
    ekle.add_argument("--baslik", required=True, help="ödevin başlığı")
    ekle.add_argument("--teslim", required=True, help="teslim tarihi (YYYY-AA-GG)")
    ekle.set_defaults(islem=_ekle)
    return parser


def _utf8_cikti():
    """Windows'ta çıktı yönlendirildiğinde Türkçe karakterler bozulmasın."""
    for akis in (sys.stdout, sys.stderr):
        if hasattr(akis, "reconfigure") and (akis.encoding or "").lower() != "utf-8":
            akis.reconfigure(encoding="utf-8")


def main(argv=None):
    _utf8_cikti()
    args = parser_olustur().parse_args(argv)
    yol = depo.dosya_yolu(args.dosya)
    try:
        args.islem(args, yol)
    except (OdevHatasi, depo.DepoHatasi) as hata:
        print(f"Hata: {hata}", file=sys.stderr)
        return 1
    return 0
