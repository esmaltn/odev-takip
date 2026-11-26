from datetime import date

import pytest

from odev_takip import cli
from odev_takip.cli import main
from odev_takip.listeleme import kalan_sure_metni, liste_satirlari

BUGUN = date(2026, 11, 26)


@pytest.fixture
def sabit_bugun(monkeypatch):
    monkeypatch.setattr(cli, "bugun", lambda: BUGUN)


def _ekle(dosya, ders, baslik, teslim):
    komut = ["--dosya", str(dosya), "ekle", "--ders", ders, "--baslik", baslik, "--teslim", teslim]
    assert main(komut) == 0


@pytest.mark.parametrize(
    "teslim,beklenen",
    [
        (date(2026, 11, 27), "1 gün kaldı"),
        (date(2026, 12, 6), "10 gün kaldı"),
        (date(2026, 11, 26), "BUGÜN"),
        (date(2026, 11, 25), "GECİKTİ (1 gün)"),
        (date(2026, 11, 20), "GECİKTİ (6 gün)"),
    ],
)
def test_kalan_sure_metni(teslim, beklenen):
    assert kalan_sure_metni(teslim, BUGUN) == beklenen


def test_bos_listede_mesaj_verilir(tmp_path, capsys, sabit_bugun):
    assert main(["--dosya", str(tmp_path / "yok.json"), "listele"]) == 0
    assert capsys.readouterr().out.strip() == "Kayıtlı ödev yok."


def test_odevler_teslim_tarihine_gore_artan_sirada_listelenir(tmp_path, capsys, sabit_bugun):
    dosya = tmp_path / "odevler.json"
    _ekle(dosya, "Fizik", "Lab raporu", "2026-12-10")
    _ekle(dosya, "Matematik", "Problem seti", "2026-11-20")
    _ekle(dosya, "Veri Yapıları", "Ödev 2", "2026-11-26")
    capsys.readouterr()

    assert main(["--dosya", str(dosya), "listele"]) == 0
    satirlar = capsys.readouterr().out.strip().splitlines()
    assert satirlar == [
        "[2] 2026-11-20 | Matematik | Problem seti | GECİKTİ (6 gün)",
        "[3] 2026-11-26 | Veri Yapıları | Ödev 2 | BUGÜN",
        "[1] 2026-12-10 | Fizik | Lab raporu | 14 gün kaldı",
    ]


def test_ayni_tarihte_eklenme_sirasi_korunur():
    odevler = [
        {"id": 1, "ders": "A", "baslik": "x", "teslim": "2026-12-01"},
        {"id": 2, "ders": "B", "baslik": "y", "teslim": "2026-12-01"},
    ]
    satirlar = liste_satirlari(odevler, BUGUN)
    assert satirlar[0].startswith("[1]") and satirlar[1].startswith("[2]")


def test_dosya_parametresi_alt_komuttan_sonra_da_calisir(tmp_path, capsys, sabit_bugun):
    dosya = tmp_path / "odevler.json"
    _ekle(dosya, "Fizik", "Lab", "2026-11-30")
    capsys.readouterr()
    assert main(["listele", "--dosya", str(dosya)]) == 0
    assert "4 gün kaldı" in capsys.readouterr().out
