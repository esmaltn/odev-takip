# Proje Panosu

Pano: **https://github.com/users/esmaltn/projects/3** (herkese açık)

Sütunlar (Status alanı): **Yapılacak**, **Devam Ediyor**, **Tamamlandı**.
Her kart bu depodaki bir issue'dur; açıklama ve kabul kriterleri issue'nun içindedir.
Geliştirilen kartlarda commit ve PR bağlantıları hem issue'da hem de panodaki
"Bağlantı" alanında yer alır.

| # | Kart | Sütun | Bağlantılar |
|---|------|-------|-------------|
| [#1](https://github.com/esmaltn/odev-takip/issues/1) | Ödev ekleme | Tamamlandı | [commit f626ff0](https://github.com/esmaltn/odev-takip/commit/f626ff0ed1aba1c5fb295b9e4358bc2eccf59035), [PR #6](https://github.com/esmaltn/odev-takip/pull/6) |
| [#2](https://github.com/esmaltn/odev-takip/issues/2) | Ödevleri listeleme | Tamamlandı | [commit eacd449](https://github.com/esmaltn/odev-takip/commit/eacd449e75f99097b7a9acec0e8cb8429b57f9ca), [PR #7](https://github.com/esmaltn/odev-takip/pull/7) |
| [#3](https://github.com/esmaltn/odev-takip/issues/3) | Ödevi tamamlandı olarak işaretleme | Yapılacak | – |
| [#4](https://github.com/esmaltn/odev-takip/issues/4) | Ödev silme | Yapılacak | – |
| [#5](https://github.com/esmaltn/odev-takip/issues/5) | Derse göre filtreleme | Yapılacak | – |

## Kartlar

### 1. Ödev ekleme — Tamamlandı
Öğrenci, `ekle --ders X --baslik Y --teslim YYYY-AA-GG` komutuyla yeni bir ödevi JSON dosyasına kaydedebilmeli.

Kabul kriterleri:
- [x] Komut ödevi dosyaya kaydeder ve `Eklendi: ...` yazar.
- [x] Geçersiz tarih (ör. `2026-02-30`, `15-12-2026`) açıklayıcı bir hata mesajıyla reddedilir ve hiçbir şey kaydedilmez.
- [x] Boş (ya da yalnızca boşluktan oluşan) ders adı veya başlık açıklayıcı bir hatayla reddedilir.
- [x] Dosya `--dosya` parametresi ya da `ODEV_DOSYA` ortam değişkeniyle değiştirilebilir; varsayılan `odevler.json`.
- [x] Testler pytest ile yazılmış ve CI'da geçiyor.

### 2. Ödevleri listeleme — Tamamlandı
Öğrenci, `listele` komutuyla tüm ödevlerini teslim tarihine göre sıralı ve kalan süreyle birlikte görebilmeli.

Kabul kriterleri:
- [x] Ödevler teslim tarihine göre artan sırada listelenir.
- [x] Her satırda `n gün kaldı`, `BUGÜN` ya da `GECİKTİ (n gün)` yazar.
- [x] Hiç ödev yoksa `Kayıtlı ödev yok.` mesajı gösterilir.
- [x] Testler pytest ile yazılmış ve CI'da geçiyor.

### 3. Ödevi tamamlandı olarak işaretleme — Yapılacak
Öğrenci, teslim ettiği bir ödevi numarasıyla tamamlandı olarak işaretleyebilmeli.

Kabul kriterleri:
- [ ] `tamamla <id>` komutu ilgili ödevin `tamamlandi` alanını `true` yapar ve onay mesajı yazar.
- [ ] Var olmayan bir numara verilirse açıklayıcı bir hata gösterilir.
- [ ] Tamamlanan ödevler `listele` çıktısında `TAMAMLANDI` olarak görünür.

### 4. Ödev silme — Yapılacak
Öğrenci, yanlış girdiği ya da artık gerekmeyen bir ödevi numarasıyla silebilmeli.

Kabul kriterleri:
- [ ] `sil <id>` komutu ilgili ödevi dosyadan kaldırır ve `Silindi: ...` yazar.
- [ ] Var olmayan bir numara verilirse açıklayıcı bir hata gösterilir ve dosya değişmez.

### 5. Derse göre filtreleme — Yapılacak
Öğrenci, yalnızca belirli bir dersin ödevlerini listeleyebilmeli.

Kabul kriterleri:
- [ ] `listele --ders X` yalnızca ders adı X olan ödevleri (büyük/küçük harf duyarsız) gösterir.
- [ ] Eşleşen ödev yoksa `Bu derse ait ödev yok.` mesajı verilir.
