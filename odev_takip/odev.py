"""Ödev kayıtlarının oluşturulması ve doğrulanması."""

import re
from datetime import date, datetime

TARIH_BICIMI = "%Y-%m-%d"
_TARIH_DESENI = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class OdevHatasi(Exception):
    """Kullanıcının girdiği ödev bilgisi geçersiz olduğunda fırlatılır."""


def tarih_coz(metin):
    """'YYYY-AA-GG' biçimindeki metni tarihe çevirir; geçersizse OdevHatasi fırlatır."""
    metin = (metin or "").strip()
    try:
        if not _TARIH_DESENI.match(metin):
            raise ValueError
        return datetime.strptime(metin, TARIH_BICIMI).date()
    except ValueError:
        raise OdevHatasi(
            f"Geçersiz teslim tarihi: '{metin}'. Tarih YYYY-AA-GG biçiminde "
            "ve takvimde var olan bir gün olmalı (ör. 2026-12-15)."
        ) from None


def odev_olustur(odevler, ders, baslik, teslim):
    """Doğrulanmış yeni bir ödev kaydı oluşturur (listeye eklemez)."""
    ders = (ders or "").strip()
    baslik = (baslik or "").strip()
    if not ders:
        raise OdevHatasi("Ders adı boş olamaz. Örnek: --ders \"Veri Yapıları\"")
    if not baslik:
        raise OdevHatasi("Ödev başlığı boş olamaz. Örnek: --baslik \"Proje raporu\"")
    teslim_tarihi = tarih_coz(teslim)
    yeni_id = max((o.get("id", 0) for o in odevler), default=0) + 1
    return {
        "id": yeni_id,
        "ders": ders,
        "baslik": baslik,
        "teslim": teslim_tarihi.isoformat(),
        "tamamlandi": False,
    }


def odev_metni(odev):
    """Bir ödevi tek satırlık okunabilir metne çevirir."""
    return f"[{odev['id']}] {odev['ders']} - {odev['baslik']} (teslim: {odev['teslim']})"
