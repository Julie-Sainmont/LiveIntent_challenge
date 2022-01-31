# LiveIntent_challenge

## Folder structure
The python code is present in the main folder.  

Subfolders:
 - inputs: contains the database file copied from LiveIntent's repository
 - outputs: contains the outputs files from the code, it contains mainly the plots/visuls,
 - report: contains the LaTeX code to produce the report.

## Python code
The data extract, combination, analysis and creation of the visuals are run by compiling the main.py code.
The plots export is controled by the save_graph parameter in the parameters.py file.


## Report
The report is done in LateX. The .tex file can the compiled with pdflatex to produce the pdf.
To ensure that all the references get updated, the report should be compiled twice.

The figures are fetched directly in the 'outputs' folder so updates on the visuals from the python code will be automatically
reflected in the report (after it is recompiled).