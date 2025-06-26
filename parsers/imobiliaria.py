import xml.etree.ElementTree as ET
import json

def get_text(element, tag):
    child = element.find(tag)
    return child.text if child is not None else None

tree = ET.parse('parsers/imobiliaria.xml')
root = tree.getroot()

imoveis = []

for imovel in root.findall('imovel'):
    proprietario = imovel.find('proprietario')
    endereco = imovel.find('endereco')
    caracteristicas = imovel.find('caracteristicas')

    dados = {
        'descricao': get_text(imovel, 'descricao'),
        'proprietario': {
            'nome': get_text(proprietario, 'nome') if proprietario is not None else None,
            'telefones': [tel.text for tel in proprietario.findall('telefone')] if proprietario is not None else [],
            'email': get_text(proprietario, 'email') if proprietario is not None else None
        },
        'endereco': {
            'rua': get_text(endereco, 'rua') if endereco is not None else None,
            'bairro': get_text(endereco, 'bairro') if endereco is not None else None,
            'cidade': get_text(endereco, 'cidade') if endereco is not None else None,
            'numero': get_text(endereco, 'numero') if endereco is not None else None
        },
        'caracteristicas': {
            'tamanho': get_text(caracteristicas, 'tamanho') if caracteristicas is not None else None,
            'numQuartos': get_text(caracteristicas, 'numQuartos') if caracteristicas is not None else None,
            'numBanheiros': get_text(caracteristicas, 'numBanheiros') if caracteristicas is not None else None
        },
        'valor': get_text(imovel, 'valor')
    }
    imoveis.append(dados)

with open('json/imobiliaria.json', 'w', encoding='utf-8') as f:
    json.dump(imoveis, f, indent=4, ensure_ascii=False)

print("Conversão concluída. Arquivo 'json/imobiliaria.json' criado.")