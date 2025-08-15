# ReArgs

**ReArgs (not “regards”)** is a tool to help you **re-polish** or better understand an article or text.  

It works by:  
- Grouping paragraphs in a text.  
- Checking each sentence within a paragraph and grouping them according to their meaning using [sentence-transformers](https://github.com/UKPLab/sentence-transformers?tab=readme-ov-file).  
- Then grouping paragraphs in the same way.  

This allows you to:  
- Spot logic repetitions in your writing.  
- Reorganize your text to make it **clearer, more concise, and easier to read**.  
- Quickly see what an article or each paragraph is about.  

**Usage Instructions**

1. **Prepare your files**
   Place your `.txt` files directly inside the `input` folder.

   > *Note:* The script does **not** check nested folders—files must be in `input` itself.

2. **Run the program**
   Execute the shell script:

   ```bash
   ./run.sh
   ```

3. **How it works**

   * The `get_files` function will copy your `.txt` files into the `transforms` folder.
   * The `transforms` folder is where all processing happens—**do not modify** its contents manually.
   * Your original files remain untouched.

4. **Output**
   Once processing is complete, the finalized files will appear in the `output` folder.


