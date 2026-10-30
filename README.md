# 📡 AI & Tech Daily Radar

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?logo=github-actions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Data_Sources-HackerNews%20%7C%20ArXiv-orange" alt="Data Sources">
  <img src="https://img.shields.io/badge/Pipeline-Autonomous_ETL-success" alt="ETL Pipeline">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
</p>

> **AI & Tech Daily Radar**, her gün GitHub Actions üzerinde otonom olarak çalışan; HackerNews üzerindeki en sıcak teknoloji gelişmelerini ve ArXiv üzerindeki en yeni Yapay Zeka / Makine Öğrenimi (AI & ML) araştırma makalelerini toplayıp derleyen modern bir veri hattıdır (data pipeline).

---

<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `2026-10-30`

> 📊 **Bugünün Özeti:** 10 HackerNews teknoloji trendi ve 5 ArXiv AI/ML akademik makalesi tarandı.  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/2026-10-30.md`)](reports/2026-10-30.md)

#### 🔥 HackerNews Öne Çıkanlar
| Başlık | Puan | Yorum | HN Linki |
|--------|:----:|:-----:|:--------:|
| [Patrick Stewart has died](https://www.nytimes.com/2026/10/29/arts/television/patrick-stewart-dead.html) | ⭐ 3071 | 💬 654 | [Tartışma](https://news.ycombinator.com/item?id=50294702) |
| [We're releasing the weights of Mistral Large 4](https://mistral.ai/news/mistral-large-4-oss/) | ⭐ 1538 | 💬 404 | [Tartışma](https://news.ycombinator.com/item?id=50289418) |
| [Binance-hacker-1029 – $5.6B stolen from Binance](https://arkm.com/explorer/entity/21a94755-f604-45e5-9501-6542e23005e8) | ⭐ 1477 | 💬 954 | [Tartışma](https://news.ycombinator.com/item?id=50296470) |
| [LLM Voice](https://martinfowler.com/bliki/LLM-Voice.html) | ⭐ 503 | 💬 263 | [Tartışma](https://news.ycombinator.com/item?id=50290177) |
| [H.264 Is Magic (2016)](https://sidbala.com/h-264-is-magic/) | ⭐ 454 | 💬 151 | [Tartışma](https://news.ycombinator.com/item?id=50291054) |

#### 🤖 ArXiv AI/ML Öne Çıkan Araştırmalar
- 📄 **[Propose-Filter-Release: Scaling Noise to Typical Sensitivity via Private Filtering](http://arxiv.org/abs/2610.40654v1)**
  *An estimator can be accurate and stable on typical data, yet sensitive to a few possible records. Differentially private mechanisms commonly scale their noise to the worst-case influence of a single r...*

- 📄 **[Rethinking Neural Thickets Without Weight Perturbations](http://arxiv.org/abs/2610.40649v1)**
  *The Neural Thickets hypothesis posits that pretrained language models lie in dense neighborhoods of task-specific experts in weight space, which random Gaussian perturbations can uncover. We reproduce...*

- 📄 **[Read, Allocate, Route: Role-Coupled Tokenization for Pixel-Space Generative Transformers](http://arxiv.org/abs/2610.40647v1)**
  *Pixel-space generative Transformers typically use one token per image patch, so capturing finer detail requires more tokens and makes global attention increasingly expensive. We observe that finer det...*

#### 🗄️ Son 7 Günün Rapor Arşivi
- [📅 2026-10-30 Raporu](reports/2026-10-30.md)
- [📅 2026-10-29 Raporu](reports/2026-10-29.md)
- [📅 2026-10-28 Raporu](reports/2026-10-28.md)
- [📅 2026-10-27 Raporu](reports/2026-10-27.md)
- [📅 2026-10-26 Raporu](reports/2026-10-26.md)
- [📅 2026-10-25 Raporu](reports/2026-10-25.md)
- [📅 2026-10-24 Raporu](reports/2026-10-24.md)
<!-- LATEST_REPORT_END -->

---

## 🏗️ Mimari ve Nasıl Çalışır?

Bu sistem, harici bir sunucu veya veritabanı ihtiyacı olmadan tamamen **serverless** ve **Git-as-a-Database** yaklaşımıyla çalışacak şekilde tasarlanmıştır:

```mermaid
flowchart LR
    A["⏰ GitHub Actions Cron<br/>(Her gün UTC 06:00)"] --> B["🐍 Python Pipeline<br/>(fetch_trends.py)"]
    B --> C["📰 HackerNews API<br/>(Top 10 Tech News)"]
    B --> D["📚 ArXiv API<br/>(Latest AI/ML Papers)"]
    C --> E["📝 Rapor Üretimi<br/>(reports/YYYY-MM-DD.md)"]
    D --> E
    E --> F["📄 README Güncelleme<br/>(Özet + Son 7 Gün Arşivi)"]
    F --> G["🚀 Git Commit & Push<br/>(Otonom Versiyonlama)"]
```

### ⚙️ Çalışma Aşamaları (ETL)

1. **Extract (Çıkarma):**
   - **HackerNews Algolia API:** Günün en popüler 10 teknoloji trendini (başlık, puan, yorum sayısı, URL) çeker.
   - **ArXiv API:** Bilgisayar Bilimleri / Yapay Zeka (`cs.AI`) ve Makine Öğrenimi (`cs.LG`) kategorilerinde yayımlanan en güncel 5 akademik makaleyi (`ElementTree` XML ayrıştırıcı ile) çeker.

2. **Transform (Dönüştürme):**
   - Alınan ham veriler standart bir Markdown formatına dönüştürülür.
   - Makale özetleri optimize edilir, tablolar ve bağlantılar biçimlendirilir.
   - Son 7 günün arşiv linkleri otomatik tespit edilir.

3. **Load (Yükleme & Dağıtım):**
   - Günün tarihine özel `reports/YYYY-MM-DD.md` dosyası oluşturulur.
   - Ana dizindeki `README.md` dosyasındaki belirlenmiş işaretçiler arasına güncel özet ve arşiv tablosu işlenir.
   - Değişiklikler GitHub Actions botu tarafından depoya geri `commit` ve `push` edilir.

---

## 🚀 Yerel Kurulum ve Çalıştırma

Projeyi yerel makinenizde test etmek isterseniz:

```bash
# 1. Projeyi klonlayın
git clone https://github.com/themuhammedguler/ai-tech-radar.git
cd ai-tech-radar

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Veri hattını çalıştırın
python src/fetch_trends.py
```

Rapor oluşturulduktan sonra `reports/` dizinini ve `README.md` dosyasını inceleyebilirsiniz.

---

## 📜 Lisans

Bu proje [MIT](LICENSE) lisansı ile lisanslanmıştır.
