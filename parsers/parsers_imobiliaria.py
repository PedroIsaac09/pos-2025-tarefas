from xml.dom.minidom import parse

def obter_texto(elemento, tag, default=None):
    filhos = elemento.getElementsByTagName(tag)
    if filhos and filhos[0].firstChild:
        return filhos[0].firstChild.nodeValue
    return default

def listar_imoveis(imoveis):
    print("Lista de imóveis disponíveis:\n")
    for idx, imovel in enumerate(imoveis, start=1):
        descricao = obter_texto(imovel, 'descricao', 'Sem descrição')
        print(f"Imóvel {idx}: {descricao}")

def mostrar_detalhes(imovel):
    print("\n--- Detalhes do imóvel ---\n")


    descricao = obter_texto(imovel, 'descricao', 'Sem descrição')
    print("Descrição:", descricao)

 
    prop = imovel.getElementsByTagName('proprietario')[0]
    nome = obter_texto(prop, 'nome', 'Desconhecido')
    email = obter_texto(prop, 'email')
    telefones = [tel.firstChild.nodeValue for tel in prop.getElementsByTagName('telefone') if tel.firstChild]

    print("Proprietário(a):", nome)
    print("Email:", email if email else "(nenhum informado)")
    print("Telefones:", ", ".join(telefones) if telefones else "(nenhum informado)")


    end = imovel.getElementsByTagName('endereco')[0]
    rua = obter_texto(end, 'rua', 'Desconhecida')
    bairro = obter_texto(end, 'bairro', 'Desconhecido')
    cidade = obter_texto(end, 'cidade', 'Desconhecida')
    numero = obter_texto(end, 'numero', 'S/N')

    print("\nEndereço")
    print("Rua:", rua)
    print("Bairro:", bairro)
    print("Cidade:", cidade)
    print("Número:", numero)

  
    caract = imovel.getElementsByTagName('caracteristicas')[0]
    tamanho = obter_texto(caract, 'tamanho', 'Indefinido')
    num_quartos = obter_texto(caract, 'numQuartos', '0')
    num_banheiros = obter_texto(caract, 'numBanheiros', '0')

    print("\nCaracterísticas")
    print("Tamanho:", f"{tamanho} m²")
    print("Número de Quartos:", num_quartos)
    print("Número de Banheiros:", num_banheiros)

    
    valor = obter_texto(imovel, 'valor', 'Não informado')
    print("Valor:", valor)

def main():
    dom = parse("parsers/imobiliaria.xml")
    imobiliaria = dom.documentElement
    imoveis = imobiliaria.getElementsByTagName('imovel')

    listar_imoveis(imoveis)

    try:
        id_escolhido = int(input("\nDigite o ID do imóvel para ver mais detalhes: "))
        if 1 <= id_escolhido <= len(imoveis):
            mostrar_detalhes(imoveis[id_escolhido - 1])
        else:
            print("ID inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

if __name__ == "__main__":
    main()