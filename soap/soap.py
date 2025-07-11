import requests
from xml.dom.minidom import parseString

URL = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

def call_soap_function(action, result_tag, country_code):
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f"http://www.oorsprong.org/websamples.countryinfo/{action}"
    }

    body = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <{action} xmlns="http://www.oorsprong.org/websamples.countryinfo">
                <sCountryISOCode>{country_code}</sCountryISOCode>
            </{action}>
        </soap:Body>
    </soap:Envelope>
    """

    response = requests.post(URL, data=body.strip(), headers=headers)
    dom = parseString(response.text)

    result_nodes = [node for node in dom.getElementsByTagName("*") if node.tagName.endswith(result_tag)]

    if result_nodes and result_nodes[0].firstChild:
        return result_nodes[0].firstChild.nodeValue
    else:
        return None

def main():
    print("Escolha uma função:")
    print("1 - Ver moeda do país")
    print("2 - Ver capital do país")
    print("3 - Ver URL da bandeira do país")

    escolha = input("Digite sua escolha (1-3): ").strip()
    codigo = input("Digite o código ISO do país (ex: BR, US, FR): ").strip().upper()

    if escolha == "1":
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "http://www.oorsprong.org/websamples.countryinfo/CountryCurrency"
        }
        body = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <CountryCurrency xmlns="http://www.oorsprong.org/websamples.countryinfo">
                    <sCountryISOCode>{codigo}</sCountryISOCode>
                </CountryCurrency>
            </soap:Body>
        </soap:Envelope>
        """
        response = requests.post(URL, data=body.strip(), headers=headers)
        dom = parseString(response.text)
        result_nodes = [node for node in dom.getElementsByTagName("*") if node.tagName.endswith("CountryCurrencyResult")]
        if result_nodes:
            sISOCode = [node for node in result_nodes[0].getElementsByTagName("*") if node.tagName.endswith("sISOCode")]
            sName = [node for node in result_nodes[0].getElementsByTagName("*") if node.tagName.endswith("sName")]
            if sISOCode and sName and sISOCode[0].firstChild and sName[0].firstChild:
                print(f"A moeda de {codigo} é: {sName[0].firstChild.nodeValue} ({sISOCode[0].firstChild.nodeValue})")
            else:
                print("Não foi possível obter a moeda.")
        else:
            print("Não foi possível obter a moeda.")

    elif escolha == "2":
        resultado = call_soap_function("CapitalCity", "CapitalCityResult", codigo)
        if resultado:
            print(f"A capital de {codigo} é: {resultado}")
        else:
            print("Não foi possível obter a capital.")

    elif escolha == "3":
        resultado = call_soap_function("CountryFlag", "CountryFlagResult", codigo)
        if resultado:
            print(f"A URL da bandeira de {codigo} é: {resultado}")
        else:
            print("Não foi possível obter a bandeira.")

    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()

