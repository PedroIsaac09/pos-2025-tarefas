from xml.dom.minidom import parse

dom = parse("parsers/cardapio.xml")
cardapio = dom.documentElement
pratos = cardapio.getElementsByTagName('prato')

print('Menu de Pratos:')
for prato in pratos:
    id_prato = prato.getAttribute('id')
    nome = prato.getElementsByTagName('nome')[0].firstChild.nodeValue
    print(f"{id_prato}: {nome}")

escolha = input('\nDigite o ID do prato para ver detalhes: ').strip()
for prato in pratos:
    if prato.getAttribute('id') == escolha:
        print('\nDetalhes do prato:')
        print('Nome:', prato.getElementsByTagName('nome')[0].firstChild.nodeValue)
        print('Descrição:', prato.getElementsByTagName('descricao')[0].firstChild.nodeValue)
        ingredientes = prato.getElementsByTagName('ingrediente')
        print('Ingredientes:', ', '.join([i.firstChild.nodeValue for i in ingredientes]))
        print('Preço:', prato.getElementsByTagName('preco')[0].firstChild.nodeValue)
        print('Calorias:', prato.getElementsByTagName('calorias')[0].firstChild.nodeValue)
        print('Tempo de preparo:', prato.getElementsByTagName('tempoPreparo')[0].firstChild.nodeValue)
        break
else:
    print('ID de prato não encontrado.')