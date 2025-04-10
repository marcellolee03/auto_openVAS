import sys
from argparse import Namespace
from pathlib import Path

from gvm.protocols.gmp import Gmp
from lxml import etree


def check_args(args):
    if len(args.argv) < 2:
        print(
            "\nUso: <report_id> [nome_do_arquivo_xml]\n"
            "Exemplo:\n"
            "  gvm-script --gmp-username user --gmp-password pass socket export-xml-report.gmp.py <report_id> resultado\n"
        )
        sys.exit(1)


def main(gmp: Gmp, args: Namespace) -> None:
    check_args(args)

    report_id = args.argv[1]
    xml_filename = (args.argv[2] if len(args.argv) > 2 else args.argv[1]) + ".xml"

    response = gmp.get_report(
        report_id=report_id,
        ignore_pagination=True,
        details=True,
    )

    if response is None:
        print("Erro: resposta do GVM veio como None.")
        sys.exit(1)

    # Aqui está o segredo: extrair o elemento <report>
    report_element = response.find("report")

    if report_element is None:
        print("Erro: elemento <report> não encontrado na resposta.")
        sys.exit(1)

    # Converte o elemento <report> em XML string
    xml_string = etree.tostring(report_element, pretty_print=True, encoding="utf-8").decode("utf-8")

    # Salva no arquivo
    xml_path = Path(xml_filename).expanduser()
    xml_path.write_text(xml_string, encoding="utf-8")

    print("✅ Relatório salvo com sucesso em:", xml_path)


if __name__ == "__gmp__":
    main(gmp, args)
