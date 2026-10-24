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
### ⚡ Son Güncelleme: `2026-10-24`

> 📊 **Bugünün Özeti:** 10 HackerNews teknoloji trendi ve 5 ArXiv AI/ML akademik makalesi tarandı.  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/2026-10-24.md`)](reports/2026-10-24.md)

#### 🔥 HackerNews Öne Çıkanlar
| Başlık | Puan | Yorum | HN Linki |
|--------|:----:|:-----:|:--------:|
| [Local Wikipedia: Wikipedia, but only for things a half hour walk from you](https://edjefferson.com/localwiki/) | ⭐ 1385 | 💬 235 | [Tartışma](https://news.ycombinator.com/item?id=50202285) |
| [Kimi K3.1 Pro and K3.1 Pro Highspeed](https://www.kimi.ai/blog/kimi-k3-1-pro) | ⭐ 916 | 💬 534 | [Tartışma](https://news.ycombinator.com/item?id=50212065) |
| [Today, we hacked what we'd set out to hack: the iPhone](https://blog.calif.io/p/iphone) | ⭐ 886 | 💬 581 | [Tartışma](https://news.ycombinator.com/item?id=50211474) |
| [Apple Music 404 Not Found](https://music.apple.com/this-url-doesnt-exist) | ⭐ 765 | 💬 232 | [Tartışma](https://news.ycombinator.com/item?id=50207910) |
| [Canadians are running out of time to oppose Bill C-22](https://www.eff.org/deeplinks/2026/10/canadians-are-running-out-time-oppose-dangerous-c-22-surveillance-bill) | ⭐ 418 | 💬 220 | [Tartışma](https://news.ycombinator.com/item?id=50202114) |

#### 🤖 ArXiv AI/ML Öne Çıkan Araştırmalar
- 📄 **[Sensorimotor Alignment: A Platonic Proxy for Embodied Policy Success](http://arxiv.org/abs/2610.31670v1)**
  *Robotic foundation models are typically evaluated through costly closed-loop rollouts, which motivates cheap offline proxies for model capability. The Platonic Representation Hypothesis (PRH) suggests...*

- 📄 **[Direct Pass@$k$ Optimization for Thought Pruning: Balancing Quality and Diversity in Test-Time Reasoning](http://arxiv.org/abs/2610.31667v1)**
  *Test-time scaling has emerged as a key inference strategy for reasoning models, where a model generates a large number of candidate solutions in the hope of finding at least one correct solution. Runn...*

- 📄 **[Phase Transition from Random Features to Fully Trainable Networks](http://arxiv.org/abs/2610.31663v1)**
  *Constructing accurate and computationally tractable approximation spaces is a fundamental task in scientific computing. Partially trainable neural networks bridge fixed random features and fully adapt...*

#### 🗄️ Son 7 Günün Rapor Arşivi
- [📅 2026-10-24 Raporu](reports/2026-10-24.md)
- [📅 2026-10-23 Raporu](reports/2026-10-23.md)
- [📅 2026-10-22 Raporu](reports/2026-10-22.md)
- [📅 2026-10-21 Raporu](reports/2026-10-21.md)
- [📅 2026-10-20 Raporu](reports/2026-10-20.md)
- [📅 2026-10-19 Raporu](reports/2026-10-19.md)
- [📅 2026-10-18 Raporu](reports/2026-10-18.md)
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
