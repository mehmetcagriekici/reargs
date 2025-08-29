# ReArgs

**ReArgs (not “regards”)** is a command-line Python application that analyzes `.txt` files for semantic repetitions and similarities.
It does **not** rewrite your text for you—it simply helps you **visualize and organize** your writing by highlighting repetitions and grouping similar content.

---

## Motivation

I enjoy writing posts and articles (often on Reddit), but I noticed a recurring problem:
my drafts quickly turned into a mess because of poor planning and constant repetition.

Reading an entire article multiple times to catch repetitions was frustrating, so I built **ReArgs** to automatically surface these similarities.
It helps me:

- Write **cleaner articles** by avoiding unintentional repetition.
- **Understand other articles** better by grouping sentences and paragraphs with similar meaning.

---

## How to Use

Clone the repo and install dependencies:

Run the provided shell script with a `.txt` file as an argument:

```bash
./run.sh path/to/article.txt
```

### Notes

- The application only accepts **one `.txt` file at a time**.
- Your original file is never modified.
- Results are displayed in the console and also written to the `output/` folder.
- The `transforms/` folder is used internally—do not manually modify its contents.

---

## How It Works

1. The application copies the input file into the `transforms/` folder.
2. It splits the article into **paragraphs** and **sentences**.
3. Using [Sentence Transformers](https://github.com/UKPLab/sentence-transformers), it:

   - Finds semantic similarities within each paragraph.
   - Then checks similarities **across the entire article**.

### Similarity Clusters

- **Hard clusters (≥ 0.8 similarity):** treated as duplicates.
- **Soft clusters (0.6–0.8 similarity):** treated as sentences with close meaning.

Finally:

- A **similarity graph** and grouped results are printed to the console.
- A summary report is written to the `output/` folder.

The purpose is to highlight repetitions, not to automatically generate polished text.

---

## Disclaimer

ReArgs is a **writing assistant**, not an article generator.
It is designed to **help you improve your own writing** by making patterns more visible.
