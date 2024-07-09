import urequests
import gc

def http_request(url):
    """Realiza uma requisição HTTP GET."""
    
    print("Início do request")
    mem_info = gc.mem_free(), gc.mem_alloc()
    gc.collect()
    print("Memória livre: {} bytes".format(mem_info[0]))
    print("Memória alocada: {} bytes".format(mem_info[1]))
    response = urequests.get(url)
    print("Fim do request")
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erro na requisição: {}".format(response.status_code))