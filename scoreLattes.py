#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This is the scoreLattes script.
#
# Copyright (C) 2017 Vicente Helano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Vicente Helano <vicente.sobrinho@ufca.edu.br>
#

import xml.etree.ElementTree as ET, sys, codecs, re, optparse

class Score(object):
    """Pontuação do Currículo Lattes"""
    def __init__(self, root, inicio, fim):
        # Período considerado para avaliação
        self.__curriculo = root
        self.__numero_identificador = 0
        self.__nome_completo = ''
        self.__ano_inicio = inicio
        self.__ano_fim = fim
        self.__formacao = 0
        self.__projetos_pesquisa = 0
        self.__projetos_desenvolvimento = 0
        self.__artigos = 0
        self.__trabalhos = 0
        self.__tabela_de_qualificacao = {
            'FORMACAO-ACADEMICA-TITULACAO' : {'POS-DOUTORADO': 0, 'LIVRE-DOCENCIA': 0, 'DOUTORADO': 0, 'MESTRADO': 0},
            'PROJETO-DE-PESQUISA' : {'PESQUISA': 0, 'DESENVOLVIMENT0': 0},
            'PRODUCAO-BIBLIOGRAFICA' : {
                'ARTIGOS-PUBLICADOS': {'A1': 0, 'A2': 0, 'B1': 0, 'B2': 0, 'B3': 0, 'B4': 0, 'B5': 0, 'C': 0, 'NAO-ENCONTRADO': 0},
                'TRABALHOS-EM-EVENTOS': {
                    'INTERNACIONAL': { 'COMPLETO': 0, 'RESUMO_EXPANDIDO': 0, 'RESUMO': 0 },
                    'NACIONAL': { 'COMPLETO': 0, 'RESUMO_EXPANDIDO': 0, 'RESUMO': 0 },
                    'REGIONAL': { 'COMPLETO': 0, 'RESUMO_EXPANDIDO': 0, 'RESUMO': 0 },
                    'LOCAL': { 'COMPLETO': 0, 'RESUMO_EXPANDIDO': 0, 'RESUMO': 0 },
                    'NAO_INFORMADO': { 'COMPLETO': 0, 'RESUMO_EXPANDIDO': 0, 'RESUMO': 0 },
                },
                'LIVROS-E-CAPITULOS': {
                    'LIVRO-PUBLICADO-OU-ORGANIZADO': {
                        'LIVRO_PUBLICADO': 0,
                        'LIVRO_ORGANIZADO_OU_EDICAO': 0,
                        'NAO_INFORMADO': 0,
                    },
                    'CAPITULO-DE-LIVRO-PUBLICADO': 0,
                },
                'DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA': { 'TRADUCAO': 0 },
            },
            'PRODUCAO-TECNICA': {
                'SOFTWARE': 0,
                'PATENTE': {'DEPOSITADA': 0, 'CONCEDIDA': 0},
                'PRODUTO-TECNOLOGICO': 0,
                'PROCESSOS-OU-TECNICAS': 0,
                'TRABALHO-TECNICO': 0,
            },
            'OUTRA-PRODUCAO': {
                'PRODUCAO-ARTISTICA-CULTURAL': {
                    'APRESENTACAO-DE-OBRA-ARTISTICA': 0,
                    'COMPOSICAO-MUSICAL': 0,
                    'OBRA-DE-ARTES-VISUAIS': 0,
                },
            },
            'ORIENTACOES-CONCLUIDAS': {
                'ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO': 0,
                'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO': 0,
                'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO': 0,
            },
            'CO-ORIENTACOES-CONCLUIDAS': {
                'CO-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO': 0,
                'CO-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO': 0,
            },
            'OUTRAS-ORIENTACOES-CONCLUIDAS': {
                'MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO': 0,
                'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO': 0,
                'INICIACAO_CIENTIFICA': 0,
            },
        }
        self.__pontuacao = {
            'FORMACAO-ACADEMICA-TITULACAO' : 0,
            'PROJETO-DE-PESQUISA': 0,
            'PRODUCAO-BIBLIOGRAFICA': 0,
            'PRODUCAO-TECNICA': 0,
            'OUTRA-PRODUCAO': 0,
            'ORIENTACOES-CONCLUIDAS': 0,
            'CO-ORIENTACOES-CONCLUIDAS': 0,
            'OUTRAS-ORIENTACOES-CONCLUIDAS': 0,
        }

        # Calcula pontuação do currículo
        self.__dados_gerais()
        self.__formacao_academica_titulacao()
        self.__projetos_de_pesquisa()
#        self.__producao_bibliografica()

    def __dados_gerais(self):
        if 'NUMERO-IDENTIFICADOR' not in self.__curriculo.attrib:
            raise ValueError
        self.__numero_identificador = self.__curriculo.attrib['NUMERO-IDENTIFICADOR']

        dados = self.__curriculo.find('DADOS-GERAIS')
        self.__nome_completo = dados.attrib['NOME-COMPLETO']

    def __formacao_academica_titulacao(self):
        dados = self.__curriculo.find('DADOS-GERAIS')
        formacao = dados.find('FORMACAO-ACADEMICA-TITULACAO')
        if formacao is None:
            return
        barema = {'POS-DOUTORADO': 10, 'LIVRE-DOCENCIA': 8, 'DOUTORADO': 7, 'MESTRADO': 3}
        for key,value in barema.items():
            result = formacao.find(key)
            if result is None:
                continue
            if key == 'LIVRE-DOCENCIA': # neste caso, não há STATUS-DO-CURSO
                self.__tabela_de_qualificacao['FORMACAO-ACADEMICA-TITULACAO'][key] = value
            elif result.attrib['STATUS-DO-CURSO'] == 'CONCLUIDO':
                self.__tabela_de_qualificacao['FORMACAO-ACADEMICA-TITULACAO'][key] = value
        # Calcula a pontuação total da formação acadêmica
        self.__pontuacao['FORMACAO-ACADEMICA-TITULACAO'] = sum(self.__tabela_de_qualificacao['FORMACAO-ACADEMICA-TITULACAO'].values())
            
    def __projetos_de_pesquisa(self):
        dados = self.__curriculo.find('DADOS-GERAIS')
        if dados.find('ATUACOES-PROFISSIONAIS') is None:
            return

        atuacoes = dados.find('ATUACOES-PROFISSIONAIS').findall('ATUACAO-PROFISSIONAL')
        for atuacao in atuacoes:
            atividade = atuacao.find('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')
            if atividade is None:
                continue

            participacoes = atividade.findall('PARTICIPACAO-EM-PROJETO')
            for participacao in participacoes:
                projetos = participacao.findall('PROJETO-DE-PESQUISA')
                if projetos is None:
                    continue

                # O ano de início da participação em um projeto
                inicio_part = int(participacao.attrib['ANO-INICIO'])

                for projeto in projetos:
                    # Ignorar projeto ou participação em projeto iniciados antes do período estipulado
                    if projeto.attrib['ANO-INICIO'] != "":
                        if int(projeto.attrib['ANO-INICIO']) < self.__ano_inicio:
                            continue
                    else:
                        if inicio_part < self.__ano_inicio:
                            continue
                      
                    # Ignorar se o proponente não for o coordenador do projeto
                    equipe = (projeto.find('EQUIPE-DO-PROJETO')).find('INTEGRANTES-DO-PROJETO')
                    if equipe.attrib['FLAG-RESPONSAVEL'] != str('SIM'):
                        continue

                    # Verifica se o projeto é financiado
                    financiamento = projeto.find('FINANCIADORES-DO-PROJETO')
                    if financiamento is None:
                        continue

                    # Verifica se há órgão financiador externo, diferente de UFC e UFCA
                    codigos = ['', 'JI7500000002', '001500000997', '008900000002']
                    financiadores = financiamento.findall('FINANCIADOR-DO-PROJETO')
                    fomento_externo = False
                    for financiador in financiadores:
                        if financiador.attrib['CODIGO-INSTITUICAO'] not in codigos:
                            fomento_externo = True
                            break
                    if not fomento_externo:
                        continue
                    
                    if projeto.attrib['NATUREZA'] == 'PESQUISA':
                        if self.__tabela_de_qualificacao['PROJETO-DE-PESQUISA']['PESQUISA'] <= 6: # máximo de 8 pontos
                            self.__tabela_de_qualificacao['PROJETO-DE-PESQUISA']['PESQUISA'] += 2
                    elif projeto.attrib['NATUREZA'] == 'DESENVOLVIMENTO':
                        if self.__tabela_de_qualificacao['PROJETO-DE-PESQUISA']['DESENVOLVIMENT0'] <= 6: # máximo de 8 pontos
                            self.__tabela_de_qualificacao['PROJETO-DE-PESQUISA']['DESENVOLVIMENT0'] += 2

        # Calcula a pontuação total dos projetos de pesquisa
        self.__pontuacao['PROJETO-DE-PESQUISA'] = sum(self.__tabela_de_qualificacao['PROJETO-DE-PESQUISA'].values())

    def __producao_bibliografica(self):
        producao = self.__curriculo.find('PRODUCAO-BIBLIOGRAFICA')
        if producao is None:
            return

        self.__artigos_publicados(producao)
        self.__trabalhos_em_eventos(producao)

    def __artigos_publicados(self, producao):
        artigos = producao.find('ARTIGOS-PUBLICADOS')
        if artigos is None:
            return
        for artigo in artigos.findall('ARTIGO-PUBLICADO'):
            self.__artigos += 1

    def __trabalhos_em_eventos(self, producao):
        trabalhos = producao.find('TRABALHOS-EM-EVENTOS')
        if trabalhos is None:
            return
        for trabalho in trabalhos.findall('TRABALHO-EM-EVENTOS'):
            natureza = trabalho.find('DADOS-BASICOS-DO-TRABALHO').attrib['NATUREZA']
            abrangencia = trabalho.find('DETALHAMENTO-DO-TRABALHO').attrib['CLASSIFICACAO-DO-EVENTO']
            if natureza == 'RESUMO':
                print 'resumo'
                if abrangencia == 'INTERNACIONAL':
                    print '  nacional'
                elif abrangencia == 'NACIONAL':
                    print '  nacional'
                elif abrangencia == 'REGIONAL':
                    print '  nacional'
                elif abrangencia == 'LOCAL':
                    print '  nacional'
                else:
                    print '  ' + abrangencia
            self.__trabalhos += 1

    def sumario(self, ostream):
        #print self.__tabela_de_qualificacao
        #print ''
        print self.__nome_completo
        print self.__numero_identificador
        print "FORMACAO-ACADEMICA-TITULACAO: ".decode("utf8") + str(self.__pontuacao['FORMACAO-ACADEMICA-TITULACAO']).encode("utf-8")
        print "PROJETO-DE-PESQUISA:          ".decode("utf8") + str(self.__pontuacao['PROJETO-DE-PESQUISA']).encode("utf-8")
        print ''


def main():
    # Define program options
    optParser = optparse.OptionParser(
        usage="usage: %prog [options] XMLfile",
        version="%prog 0.1",
        description="Convert XML file exported by the Lattes CV platform to the BibTeX(ML) format.")
    optParser.add_option("-f", "--filename", dest="filename",
        help="write output to FILE (default is stdout)")
    optParser.add_option("-x", "--xml",
        action="store_true", dest="xml", default=False,
        help="output file using the BibTeXML format")
    optParser.add_option("-v", "--verbose",
        action="store_true", dest="verbose", default=False,
        help="explain what is being done")

    # Process options
    (options, args) = optParser.parse_args()

    if len(args) != 1:
        optParser.error("incorrect number of arguments\n"
            "Try `%s --help' for more information." % sys.argv[0])

    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    ostream = sys.stdout
    if options.filename:
        try:
            ostream = codecs.open(options.filename, 'w', encoding='utf-8')
        except:
            sys.stderr.write(sys.argv[0] + ': cannot create file `' + options.filename + "'.\n")
            sys.exit()

    tree = ET.parse(args[0])
    root = tree.getroot()
    score = Score(root, 2012, 2017)
    score.sumario(ostream)

# Main
if __name__ == "__main__":
    sys.exit(main())
