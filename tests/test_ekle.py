import json

import pytest

from odev_takip.cli import main
from odev_takip.odev import OdevHatasi, odev_olustur, tarih_coz


def _ekle(dosya, ders="Veri Yapıları", baslik="Ödev 1", teslim="2026-12-15"):
    return main(
        ["--dosya", str(dosya), "ekle", "--ders", ders, "--baslik", baslik, "--teslim", teslim]
    )


def test_odev_eklenir_ve_kaydedilir(tmp_path, capsys):
    dosya = tmp_path / "odevler.json"
    assert _ekle(dosya) == 0
    cikti = capsys.readouterr().out
    assert cikti.startswith("Eklendi: ")
    assert "Veri Yapıları" in cikti and "Ödev 1" in cikti and "2026-12-15" in cikti

    kayitlar = json.loads(dosya.read_text(encoding="utf-8"))
    assert kayitlar == [
        {
            "id": 1,
            "ders": "Veri Yapıları",
            "baslik": "Ödev 1",
            "teslim": "2026-12-15",
            "tamamlandi": False,
        }
    ]


def test_birden_fazla_odev_artan_id_alir(tmp_path):
    dosya = tmp_path / "odevler.json"
    _ekle(dosya, baslik="A")
    _ekle(dosya, ders="Fizik", baslik="B")
    kayitlar = json.loads(dosya.read_text(encoding="utf-8"))
    assert [k["id"] for k in kayitlar] == [1, 2]
    assert kayitlar[1]["ders"] == "Fizik"


def test_ders_ve_baslik_bosluklardan_temizlenir(tmp_path):
    dosya = tmp_path / "odevler.json"
    _ekle(dosya, ders="  Fizik  ", baslik="  Lab raporu ")
    kayit = json.loads(dosya.read_text(encoding="utf-8"))[0]
    assert kayit["ders"] == "Fizik" and kayit["baslik"] == "Lab raporu"


@pytest.mark.parametrize(
    "tarih", ["2026-02-30", "15-12-2026", "2026/12/15", "2026-1-5", "yarın", ""]
)
def test_gecersiz_tarih_reddedilir(tmp_path, capsys, tarih):
    dosya = tmp_path / "odevler.json"
    assert _ekle(dosya, teslim=tarih) == 1
    hata = capsys.readouterr().err
    assert "Geçersiz teslim tarihi" in hata and "YYYY-AA-GG" in hata
    assert not dosya.exists()


@pytest.mark.parametrize(
    "alan,mesaj", [("ders", "Ders adı boş olamaz"), ("baslik", "Ödev başlığı boş olamaz")]
)
@pytest.mark.parametrize("deger", ["", "   "])
def test_bos_ders_veya_baslik_reddedilir(tmp_path, capsys, alan, mesaj, deger):
    dosya = tmp_path / "odevler.json"
    assert _ekle(dosya, **{alan: deger}) == 1
    assert mesaj in capsys.readouterr().err
    assert not dosya.exists()


def test_ortam_degiskeni_ile_dosya_secilir(tmp_path, monkeypatch):
    dosya = tmp_path / "ortam.json"
    monkeypatch.setenv("ODEV_DOSYA", str(dosya))
    assert main(["ekle", "--ders", "Fizik", "--baslik", "Lab", "--teslim", "2026-12-01"]) == 0
    assert json.loads(dosya.read_text(encoding="utf-8"))[0]["baslik"] == "Lab"


def test_dosya_parametresi_ortam_degiskeninden_onceliklidir(tmp_path, monkeypatch):
    ortam = tmp_path / "ortam.json"
    param = tmp_path / "param.json"
    monkeypatch.setenv("ODEV_DOSYA", str(ortam))
    komut = ["ekle", "--ders", "F", "--baslik", "B", "--teslim", "2026-12-01", "--dosya", str(param)]
    assert main(komut) == 0
    assert param.exists() and not ortam.exists()


def test_bozuk_dosya_aciklayici_hata_verir(tmp_path, capsys):
    dosya = tmp_path / "odevler.json"
    dosya.write_text("{bozuk", encoding="utf-8")
    assert _ekle(dosya) == 1
    assert "geçerli bir JSON değil" in capsys.readouterr().err


def test_tarih_coz_gecerli_tarihi_dondurur():
    assert tarih_coz("2026-12-15").isoformat() == "2026-12-15"


def test_odev_olustur_gecersiz_tarihte_hata_firlatir():
    with pytest.raises(OdevHatasi):
        odev_olustur([], "Ders", "Başlık", "2026-13-01")
