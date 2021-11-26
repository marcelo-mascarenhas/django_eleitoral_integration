import json
from datetime import datetime
import copy
import os

METODOS_POSSIVEIS = ["preliminar", "naive_bayes", "rnn", "han", "lstm", "cnn"]
METODOS_CLASSICOS = ["naive_bayes"]
METODOS_DEEP_LEARNING = ["rnn", "han", "lstm", "cnn"]

#Metodos adicionados foram: CNN.

class PropagandaIdentifier():
  
    def __init__(self, configuration_file, modelpath):

        self.__configuration_file = configuration_file

        self.metodo_selecionado = self.__configuration_file["metodo_selecionado"]
        
        self.__models_path = modelpath


    '''
    # Se o metodo escolhido for invalido, mandar para a fila de erro (aqui retorna False)
    # Se algum arquivo de configuração não existir, mandar para a fila de erro (aqui retorna False)
    '''
    def is_parametros_validos(self):
        metodo_selecionado = self.__configuration_file["metodo_selecionado"]

        modelo_info = self.__configuration_file[f"modelo_{metodo_selecionado}"]

        if metodo_selecionado not in METODOS_POSSIVEIS:
            return False

        elif metodo_selecionado == "preliminar":
            for filename in [modelo_info["caminho_arquivo_reforco"], modelo_info["caminho_arquivo_pesos"], modelo_info["caminho_arquivo_blacklist"]]:
                
                if not self.__check_files(filename, metodo_selecionado):
                        return False

        elif metodo_selecionado in METODOS_CLASSICOS:
            if metodo_selecionado == "naive_bayes":
                for filename in [modelo_info["caminho_arquivo_skl"]]:
                    
                    if not self.__check_files(filename, metodo_selecionado):
                        return False
            else:
                for filename in [modelo_info["caminho_arquivo_skl"],  modelo_info["caminho_arquivo_word2vec"]]:
            
                    if not self.__check_files(filename, metodo_selecionado):
                        return False
                    
        elif metodo_selecionado in METODOS_DEEP_LEARNING:
            
            
            if metodo_selecionado == "cnn":
                for filename in [modelo_info["caminho_arquivo_npy"],  modelo_info["caminho_arquivo_h5"]]:
            
                    if not self.__check_files(filename, metodo_selecionado):
                        return False                
            else:
                for filename in [modelo_info["caminho_arquivo_npy"], modelo_info["caminho_arquivo_h5"], modelo_info["caminho_arquivo_word2vec"]]:

                    if not self.__check_files(filename, metodo_selecionado):
                        return False
            
        return True

    def __check_files(self, rel_path, selected_method):
        abs_path = self.__get_full_path(rel_path)
        if os.path.isfile(abs_path) is False:
            print(f"Parametros invalidos: metodo_selecionado == {selected_method} nao tem arquivos validos")
            return False

        return True
    
    def __get_full_path(self, rel_path):
        abs_path = os.path.join(self.__models_path, rel_path)
        return abs_path

    def escreve_score_metodo(self, message):

        try:
            if self.metodo_selecionado == "preliminar":

                from .metodo_preliminar import MetodoPreliminar
                info_metodo = self.__configuration_file["modelo_preliminar"]


                metodoPreliminar= MetodoPreliminar(caminho_arquivo_reforco = self.__get_full_path(info_metodo["caminho_arquivo_reforco"]),
                                                   caminho_arquivo_pesos= self.__get_full_path(info_metodo["caminho_arquivo_pesos"]),
                                                   caminho_arquivo_blacklist= self.__get_full_path(info_metodo["caminho_arquivo_blacklist"]))

                score, mensagem_erro = metodoPreliminar.get_score(texto=message)

            else:
                from .metodo_aprendizado_maquina import MetodoAprendizadoMaquina
                info_metodo = self.__configuration_file[f"modelo_{self.metodo_selecionado}"]


                if self.metodo_selecionado in METODOS_CLASSICOS:
                    caminho_arquivo_modelo = self.__get_full_path(info_metodo["caminho_arquivo_skl"])
                    caminho_arquivo_word2vec = None
                    caminho_arquivo_npy = None
                    if self.metodo_selecionado != "naive_bayes":
                        caminho_arquivo_word2vec = self.__get_full_path(info_metodo["caminho_arquivo_word2vec"])

                else:
                    caminho_arquivo_modelo = self.__get_full_path(info_metodo["caminho_arquivo_h5"])
                    caminho_arquivo_npy = self.__get_full_path(info_metodo["caminho_arquivo_npy"])
                    caminho_arquivo_word2vec = None
                    if self.metodo_selecionado != "cnn":
                        caminho_arquivo_word2vec = self.__get_full_path(info_metodo["caminho_arquivo_word2vec"])

                metodoAM = MetodoAprendizadoMaquina(
                    nome_modelo=self.metodo_selecionado,
                    caminho_arquivo_modelo=caminho_arquivo_modelo,
                    caminho_arquivo_npy=caminho_arquivo_npy,
                    caminho_arquivo_word2vec=caminho_arquivo_word2vec)

                score, mensagem_erro = metodoAM.get_score(texto=message)


            if mensagem_erro is not None:
                raise Exception(f'{mensagem_erro}. Falha na classificação')
            else:
                return score
            
        except Exception as e:
            
            raise Exception(f"{e}. Erro durante o processo de classificação.")

if __name__ == "__main__":
    pass
