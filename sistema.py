import random
from collections import deque
from itertools import combinations
import os # Usado para limpar a tela

# As classes Time, Partida e Campeonato permanecem exatamente as mesmas.


class Time:
    def __init__(self, nome):
        self.nome = nome
        self.pontos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.gols_pro = 0
        self.gols_contra = 0

    def registrar_partida(self, gols_feitos, gols_sofridos):
        self.gols_pro += gols_feitos
        self.gols_contra += gols_sofridos
        if gols_feitos > gols_sofridos:
            self.pontos += 3
            self.vitorias += 1
        elif gols_feitos == gols_sofridos:
            self.pontos += 1
            self.empates += 1
        else:
            self.derrotas += 1

    @property
    def saldo_de_gols(self):
        return self.gols_pro - self.gols_contra #gols feitos - gols sofridos= saldo de gols

    def __str__(self):
        return (f"{self.nome:<15} | P: {self.pontos:2} | V: {self.vitorias:2} | "
                f"E: {self.empates:2} | D: {self.derrotas:2} | SG: {self.saldo_de_gols:3}")

class Partida:
    def __init__(self, time_casa, time_fora):
        self.time_casa = time_casa
        self.time_fora = time_fora
        self.realizada = False

    def registrar_resultado(self, gols_casa, gols_fora):
        self.gols_casa = gols_casa #resultado do placar
        self.gols_fora = gols_fora #resultado do placar
        self.realizada = True #atualiza
        self.time_casa.registrar_partida(gols_casa, gols_fora)
        self.time_fora.registrar_partida(gols_fora, gols_casa)

class Campeonato:
    def __init__(self, nome):
        self.nome = nome
        self.times = [] #lista dinâmica
        self.partidas_agendadas = deque() #fila(deque)

    def adicionar_time(self, time):
        self.times.append(time) #adiciona ao final da lista

    def gerar_partidas(self):
        self.partidas_agendadas.clear()
        for time1, time2 in combinations(self.times, 2): #gera pares de times
            self.partidas_agendadas.append(Partida(time1, time2)) #para cada par cria uma nova partida

    def realizar_proxima_partida(self, gols_casa, gols_fora):
        if not self.partidas_agendadas: #não processar o jogo se a fila estiver vazia
            return
        proxima_partida = self.partidas_agendadas.popleft()
        proxima_partida.registrar_resultado(gols_casa, gols_fora)

    def exibir_tabela(self):
        times_ordenados = sorted(self.times, key=lambda t: (-t.pontos, -t.vitorias, -t.saldo_de_gols)) #para cada time é criado uma tupla
        print("\n" + "="*55)
        print(f" TABELA DE CLASSIFICAÇÃO: {self.nome.upper()}") #cria um cabeçalho e percorre a lista
        print("="*55)
        for time in times_ordenados:
            print(time)
        print("="*55 + "\n")

# --- BLOCO PRINCIPAL INTERATIVO ---
def main():
    """Função principal que gerencia a interação com o usuário."""
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela do terminal
    print("--- GERENCIADOR DE CAMPEONATO ESPORTIVO ---")
    
    nome_campeonato = input("Digite o nome do campeonato: ")
    campeonato = Campeonato(nome_campeonato)

    # Laço para adicionar times
    print("\nAdicione os times participantes.")
    while True: #loop infinito (laço)
        nome_time = input(f"Digite o nome do time {len(campeonato.times) + 1} (ou digite 'fim' para parar): ")
        if nome_time.lower() == 'fim':
            if len(campeonato.times) < 2:
                print("ERRO: É preciso ter pelo menos 2 times para iniciar um campeonato.")
                continue # Pede para adicionar mais um time
            else:
                break # Sai do laço se tiver times suficientes
        elif not nome_time.strip(): # Verifica se o nome não está vazio
             print("ERRO: O nome do time não pode ser vazio.")
        else:
            campeonato.adicionar_time(Time(nome_time))

    # Gera e inicia as partidas
    print("\nTimes adicionados! Gerando as partidas...")
    campeonato.gerar_partidas()
    
    total_partidas = len(campeonato.partidas_agendadas)
    partida_atual = 0

    # Laço para registrar os resultados das partidas
    while campeonato.partidas_agendadas:
        partida_atual += 1
        # Pega a próxima partida da fila sem removê-la ainda
        proxima_partida = campeonato.partidas_agendadas[0] 
        
        print(f"\n--- Partida {partida_atual}/{total_partidas} ---")
        print(f"Jogo: {proxima_partida.time_casa.nome} vs {proxima_partida.time_fora.nome}")
        
        # Validação de input para os gols
        while True:
            try:
                gols_casa = int(input(f"Gols de {proxima_partida.time_casa.nome}: "))
                gols_fora = int(input(f"Gols de {proxima_partida.time_fora.nome}: "))
                if gols_casa < 0 or gols_fora < 0:
                    print("ERRO: O número de gols não pode ser negativo. Tente novamente.")
                    continue
                break # Sai do laço de validação se os números forem válidos
            except ValueError:
                print("ERRO: Por favor, digite apenas números inteiros.")

        campeonato.realizar_proxima_partida(gols_casa, gols_fora)
        campeonato.exibir_tabela()
        input("Pressione Enter para continuar para a próxima partida...")
        os.system('cls' if os.name == 'nt' else 'clear')

    print("--- CAMPEONATO FINALIZADO! ---")
    print("Esta é a classificação final:")
    campeonato.exibir_tabela()


if __name__ == "__main__":
    main()