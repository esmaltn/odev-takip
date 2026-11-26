# Ödev Takipçisi

[![CI](https://github.com/esmaltn/odev-takip/actions/workflows/ci.yml/badge.svg)](https://github.com/esmaltn/odev-takip/actions/workflows/ci.yml)

## Proje ne işe yarar?

Aynı dönemde birden fazla ders alan üniversite öğrencileri, farklı derslerden gelen
ödevlerin teslim tarihlerini takip etmekte zorlanır; bir ödevin unutulması ya da
son güne kalması sık yaşanan bir sorundur. **Ödev Takipçisi**, bu öğrenciler için
geliştirilmiş basit bir komut satırı aracıdır: ödevleri ders adı, başlık ve teslim
tarihiyle kaydeder, ardından hepsini teslim tarihine göre sıralayarak her birine
kaç gün kaldığını ya da kaç gün geciktiğini tek bakışta gösterir.

Araç yalnızca Python standart kütüphanesini kullanır; veriler yerel bir JSON
dosyasında saklanır, internet bağlantısı ya da hesap gerektirmez.

## Proje panosu

Görevler GitHub Projects panosunda takip edilir (Yapılacak / Devam Ediyor / Tamamlandı):
**https://github.com/users/esmaltn/projects/3**

Panodaki kartların özeti ve bağlantıları için [PANO.md](PANO.md) dosyasına bakabilirsiniz.

## Kurulum ve çalıştırma

Gereksinim: Python 3.9 veya üzeri. Uygulama yalnızca standart kütüphaneyi kullanır,
ek paket kurmanız gerekmez (testler için yalnızca `pytest` gerekir).

```bash
git clone https://github.com/esmaltn/odev-takip.git
cd odev-takip
python -m odev_takip --help
```

Ödevler varsayılan olarak bulunduğunuz klasördeki `odevler.json` dosyasında saklanır.
Başka bir dosya kullanmak için `--dosya` parametresini ya da `ODEV_DOSYA` ortam
değişkenini kullanabilirsiniz (`--dosya` önceliklidir):

```bash
python -m odev_takip --dosya benim_odevlerim.json listele
ODEV_DOSYA=benim_odevlerim.json python -m odev_takip listele        # Linux / macOS / Git Bash
$env:ODEV_DOSYA = "benim_odevlerim.json"; python -m odev_takip listele  # Windows PowerShell
```

### Testleri çalıştırma

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Testler her push ve pull request'te GitHub Actions ile otomatik çalışır
([CI geçmişi](https://github.com/esmaltn/odev-takip/actions)).

## Özellikleri deneme

Aşağıdaki komutlar deneme için ayrı bir `deneme.json` dosyası kullanır; böylece
gerçek ödev listeniz etkilenmez.

### Özellik 1 – Ödev ekleme

```bash
python -m odev_takip --dosya deneme.json ekle --ders "Veri Yapıları" --baslik "Ödev 2" --teslim 2026-12-15
# Eklendi: [1] Veri Yapıları - Ödev 2 (teslim: 2026-12-15)
```

Geçersiz girdiler açıklayıcı bir hatayla reddedilir ve hiçbir şey kaydedilmez:

```bash
python -m odev_takip --dosya deneme.json ekle --ders "Fizik" --baslik "Lab" --teslim 2026-02-30
# Hata: Geçersiz teslim tarihi: '2026-02-30'. Tarih YYYY-AA-GG biçiminde ve takvimde var olan bir gün olmalı (ör. 2026-12-15).

python -m odev_takip --dosya deneme.json ekle --ders "" --baslik "Lab" --teslim 2026-12-01
# Hata: Ders adı boş olamaz. Örnek: --ders "Veri Yapıları"

python -m odev_takip --dosya deneme.json ekle --ders "Fizik" --baslik "" --teslim 2026-12-01
# Hata: Ödev başlığı boş olamaz. Örnek: --baslik "Proje raporu"
```

> Not: Windows PowerShell 5.1 boş tırnağı (`""`) programa hiç iletmez. Orada boş
> değeri denemek için `--ders " "` (yalnızca boşluk) kullanın; o da aynı hatayı verir.

### Özellik 2 – Listeleme

```bash
python -m odev_takip --dosya bos.json listele
# Kayıtlı ödev yok.

python -m odev_takip --dosya deneme.json ekle --ders "Fizik" --baslik "Lab raporu" --teslim 2026-12-10
python -m odev_takip --dosya deneme.json ekle --ders "Matematik" --baslik "Problem seti" --teslim 2026-11-20
python -m odev_takip --dosya deneme.json listele
```

Ödevler teslim tarihine göre artan sırada listelenir. Örneğin bugün 2026-11-26 ise:

```
[3] 2026-11-20 | Matematik | Problem seti | GECİKTİ (6 gün)
[2] 2026-12-10 | Fizik | Lab raporu | 14 gün kaldı
[1] 2026-12-15 | Veri Yapıları | Ödev 2 | 19 gün kaldı
```

Teslimi bugün olan bir ödev `BUGÜN` olarak gösterilir. Kalan gün sayıları
komutu çalıştırdığınız güne göre hesaplanır.

## Proje yapısı

```
odev_takip/
  __main__.py   # python -m odev_takip giriş noktası
  cli.py        # komut satırı arayüzü (argparse)
  depo.py       # JSON dosyasına okuma/yazma
  odev.py       # ödev oluşturma ve doğrulama (ekle)
  listeleme.py  # sıralama ve kalan süre hesabı (listele)
tests/          # pytest testleri
.github/workflows/ci.yml  # GitHub Actions CI
```
