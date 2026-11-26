"""Ödevlerin teslim tarihine göre sıralanıp kalan süreyle gösterilmesi."""

from datetime import date


def kalan_sure_metni(teslim, bugun):
    """Teslim tarihine göre 'n gün kaldı', 'BUGÜN' ya da 'GECİKTİ (n gün)' döner."""
    fark = (teslim - bugun).days
    if fark > 0:
        return f"{fark} gün kaldı"
    if fark == 0:
        return "BUGÜN"
    return f"GECİKTİ ({-fark} gün)"


def sirala(odevler):
    """Ödevleri teslim tarihine göre artan sırada döner (eşitlikte eklenme sırası)."""
    return sorted(odevler, key=lambda o: (o["teslim"], o.get("id", 0)))


def liste_satirlari(odevler, bugun):
    """Her ödev için ekrana yazılacak satırı üretir."""
    satirlar = []
    for odev in sirala(odevler):
        teslim = date.fromisoformat(odev["teslim"])
        durum = kalan_sure_metni(teslim, bugun)
        satirlar.append(
            f"[{odev['id']}] {odev['teslim']} | {odev['ders']} | {odev['baslik']} | {durum}"
        )
    return satirlar
