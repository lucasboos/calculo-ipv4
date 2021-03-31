import re


class CalculoIPv4:
    def __init__(self, ip, mascara=None, prefixo=None):
        self.ip = ip
        self.mascara = mascara
        self.prefixo = prefixo

        if mascara is None and prefixo is None:
            # Se nenhum valor for enviado levanta a exceção.
            raise ValueError('É nescessário enviar a máscara ou o prefixo')

        if mascara and prefixo:
            # Se ambos forem enviados levanta a exceção.
            raise ValueError(
                'É nescessário enviar apenas a máscara ou o prefixo.')

        self._set_broadcast()
        self._set_rede()

    # Getter's
    @property
    def rede(self):
        return self._rede

    @property
    def broadcast(self):
        return self._broadcast

    @property
    def numero_ips(self):
        return self._get_numero_ips()

    @property
    def ip(self):
        return self._ip

    @property
    def mascara(self):
        return self._mascara

    @property
    def prefixo(self):
        if self._prefixo is None:
            return

        return self._prefixo

    # Setter's
    @ip.setter
    def ip(self, valor):
        # É feita a validação do IP.
        if not self._valida_ip(valor):
            raise ValueError(f'O endereço de IP: {valor} está incorreto.')

        self._ip = valor
        # Transforma o IP em binário através da função.
        self._ip_bin = self._ip_to_bin(valor)

    @mascara.setter
    def mascara(self, valor):
        if not valor:
            return

        if not self._valida_ip(valor):
            raise ValueError(f'Máscara {valor} está incorreta.')

        self._mascara = valor
        self._mascara_bin = self._ip_to_bin(valor)

        # Se não foi enviado o prefixo, adiciona.
        if not hasattr(self, 'prefixo'):
            self.prefixo = self._mascara_bin.count('1')

    @prefixo.setter
    def prefixo(self, valor):
        if valor is None:
            return

        try:
            valor = int(valor)
        except:
            raise ValueError('Prefixo precisa ser um inteiro.')

        if valor > 32 or valor < 0:
            raise TypeError('Prefixo precisa ter 32Bits.')

        self._prefixo = valor

        # Multiplica o prefixo por strings de '1' e usa o método "ljust"
        # para preencher a máscara com zeros até chegar em 32 bits.
        self._mascara_bin = (valor * '1').ljust(32, '0')

        # Se não foi enviado a máscara, adiciona.
        if not hasattr(self, 'mascara'):
            self.mascara = self._bin_to_ip(self._mascara_bin)

    @staticmethod
    def _valida_ip(ip):
        # Compila o padrão a ser validado em 4 grupos de 1 a 3 números,
        # podendo variar entre 0 a 9.
        regexp = re.compile(
            r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$'
        )

        # Checa se está dentro do padrão requerido.
        if regexp.search(ip):
            return True

    @staticmethod
    def _ip_to_bin(ip):
        # Irá separar o IP através dos pontos existentes nele.
        blocos = ip.split('.')

        # Foi usado list comprehension para interagir com cada um dos blocos,
        # assim fazendo o casting para inteiro e convertendo para binário.
        # "zfill(8)" método para adicionar zeros, assim formando os 8 bits
        # nescessários em cada bloco.
        # "[2:]" para remover o "0b" padrão da conversão.
        blocos_bin = [bin(int(bloco))[2:].zfill(8) for bloco in blocos]

        # Faz a junção de todos os bits.
        blocos_bin_str = ''.join(blocos_bin)

        # Comprimento total do IP em binário para fazer a validação.
        qtd_bits = len(blocos_bin_str)

        if qtd_bits > 32:
            raise ValueError('IP ou máscara tem mais que 32 bits.')

        return blocos_bin_str

    @staticmethod
    def _bin_to_ip(ip):
        # Irá fatiar o binário gerando 4 blocos de 8 bits, fazendo o casting de
        # cada bloco para decimal. Terminando com um casting para string assim
        # transformando em um IP padrão.
        blocos = [str(int(ip[i:8 + i], 2)) for i in range(0, 32, 8)]
        return '.'.join(blocos)

    def _set_broadcast(self):
        host_bits = 32 - self.prefixo
        # Fatia o IP em binário do índice 0 até o número do prefixo,
        # fazendo a soma com o restante dos '1' em string.
        self._broadcast_bin = self._ip_bin[:self.prefixo] + (host_bits * '1')

        # Faz a conversão de binário para o IP padrão em decimal.
        self._broadcast = self._bin_to_ip(self._broadcast_bin)
        return self._broadcast

    def _set_rede(self):
        host_bits = 32 - self.prefixo
        # Fatia o IP em binário do índice 0 até o número do prefixo,
        # fazendo a soma com o restante dos '0' em string.
        self._rede_bin = self._ip_bin[:self.prefixo] + (host_bits * '0')

        # Faz a conversão de binário para o IP padrão em decimal.
        self._rede = self._bin_to_ip(self._rede_bin)
        return self._rede

    def _get_numero_ips(self):
        return 2 ** (32 - self.prefixo)
