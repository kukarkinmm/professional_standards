import argparse

from src.models.model import Model
from src.parsers.pdf_parser import PdfParser


def get_args():
    parser = argparse.ArgumentParser("Suggests most suitable professional standard")
    parser.add_argument("--rpd_path", type=str, help="path to rpd file", default="")
    parser.add_argument("--cmd_text", type=str, help="text of input", default="")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    parser = PdfParser()
    model = Model()

    text = None
    if args.rpd_path.endswith(".pdf"):
        text = parser.extract_relevant(args.rpd_path)
    elif args.rpd_path.endswith(".txt"):
        with open(args.rpd_path, 'r', encoding='utf-8') as f:
            text = "\n".join([line for line in f])
    elif args.cmd_text:
        text = args.cmd_text

    if text is not None and text != "":
        results = model.closest_standards(text)
        print("\n".join([f"{r[1]}\t-\t{r[0]}\n" for r in results]))
    else:
        print("Wrong data")
