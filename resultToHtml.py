#!/usr/bin/env python3

import csv
import html
import argparse
import sys

TEMPLATE_FILE = "template.html"
EXCLUDE_COLUMNS = ["User", "Team", "P"]
NAME_MAPPING = {
    "Username": "Lietotājvārds",
    "User": "Vārds",
    "Team": "Skola",
    "Global": "Summa"
}


def convert_result_to_html(input_name, output, template, title, description):
    with open(template, "r") as templateFile:
        template_data = templateFile.read()
    table = ""
    with open(input_name, "r") as input_file:
        reader = csv.reader(input_file)
        rows = list(reader)
        columns = []
        table += "<tr>"
        global_column = -2
        for i, name in enumerate(rows[0]):
            if name in EXCLUDE_COLUMNS:
                continue
            if name == "Global":
                global_column = i
            columns.append(i)
            column_name = NAME_MAPPING.get(name, name)
            table += "<th>{0}</th>".format(html.escape(column_name))
        table += "</tr>\n"
        results = sorted(rows[1:], reverse=True, key=lambda x: float(x[global_column]))
        for row in results:
            table += "<tr>"
            for col_id in columns:
                if col_id > 2:  # score
                    table += "<td align='right'>{0}</td>".format(html.escape(row[col_id]))
                else:
                    table += "<td>{0}</td>".format(html.escape(row[col_id]))
            table += "</tr>\n"
    args = {
        "table": table,
        "title": title,
        "description": description
    }
    result = template_data.format(**args)
    output.write(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Ouptut file")
    parser.add_argument("-t", "--title", default="Rezultāti", help="Page title")
    parser.add_argument("-d", "--description", default="")
    parser.add_argument("--template", default=TEMPLATE_FILE, help="Template html.")
    parser.add_argument('input', help="Input csv file")
    args = parser.parse_args()

    if args.output:
        with open(args.output, "w") as out_file:
            convert_result_to_html(args.input, out_file, args.template, args.title, args.description)
    else:
        convert_result_to_html(args.input, sys.stdout, args.template, args.title, args.description)


if __name__ == "__main__":
    main()
