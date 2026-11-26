"""Ödevlerin JSON dosyasında saklanması."""

import json
import os
from pathlib import Path

VARSAYILAN_DOSYA = "odevler.json"
ORTAM_DEGISKENI = "ODEV_DOSYA"


class DepoHatasi(Exception):
    """Ödev dosyası okunamadığında ya da bozuk olduğunda fırlatılır."""


def dosya_yolu(arguman=None):
    """Kullanılacak dosyayı seçer: önce --dosya, sonra ODEV_DOSYA, en son varsayılan."""
    return Path(arguman or os.environ.get(ORTAM_DEGISKENI) or VARSAYILAN_DOSYA)


def yukle(yol):
    """Ödev listesini dosyadan okur. Dosya yoksa boş liste döner."""
    yol = Path(yol)
    if not yol.exists():
        return []
    try:
        veri = json.loads(yol.read_text(encoding="utf-8") or "[]")
    except json.JSONDecodeError as hata:
        raise DepoHatasi(f"'{yol}' dosyası geçerli bir JSON değil: {hata}") from hata
    if not isinstance(veri, list):
        raise DepoHatasi(f"'{yol}' dosyası bir ödev listesi içermiyor.")
    return veri


def kaydet(yol, odevler):
    """Ödev listesini dosyaya yazar (önce geçici dosyaya yazıp sonra değiştirir)."""
    yol = Path(yol)
    if yol.parent != Path(""):
        yol.parent.mkdir(parents=True, exist_ok=True)
    gecici = yol.with_name(yol.name + ".tmp")
    gecici.write_text(
        json.dumps(odevler, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(gecici, yol)
