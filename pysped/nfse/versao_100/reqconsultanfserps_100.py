# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from pysped.xml_sped import *
from pysped.nfse.versao_100 import ESQUEMA_ATUAL
import os

DIRNAME = os.path.dirname(__file__)


class RPSConsulta(XMLNFe):
    def __init__(self):
        super(RPSConsulta, self).__init__()
        self.Id = TagCaracter(nome='RPS', propriedade='Id', raiz='//')
        self.InscricaoMunicipalPrestador = TagCaracter(nome='InscricaoMunicipalPrestador', tamanho=[ 6,  11]   , raiz='//RPS')
        self.NumeroRPS                   = TagInteiro(nome='NumeroRPS'                   , tamanho=[ 1,  12, 1], raiz='//RPS')
        self.SeriePrestacao              = TagCaracter(nome='SeriePrestacao'             , tamanho=[ 2,  2]    , raiz='//RPS', valor='99')
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        
        if self.Id.valor == '':
            self.Id.valor = 'rps:' + unicode(self.NumeroRPS.valor)
            
        xml += self.Id.xml
        xml += self.InscricaoMunicipalPrestador.xml
        xml += self.NumeroRPS.xml
        xml += self.SeriePrestacao.xml
        xml += '</RPS>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Id.xml = arquivo
            self.InscricaoMunicipalPrestador.xml = arquivo
            self.NumeroRPS.xml = arquivo
            self.SeriePrestacao.xml = arquivo

    xml = property(get_xml, set_xml)
    
    
class NotaConsulta(XMLNFe):
    def __init__(self):
        super(NotaConsulta, self).__init__()
        self.Id = TagCaracter(nome='Nota', propriedade='Id', raiz='//')
        self.InscricaoMunicipalPrestador = TagCaracter(nome='InscricaoMunicipalPrestador', tamanho=[ 6,  11]   , raiz='//Nota')
        self.NumeroNota                  = TagInteiro(nome='NumeroNota'                  , tamanho=[ 1,  12, 1], raiz='//Nota')
        self.CodigoVerificacao           = TagCaracter(nome='CodigoVerificacao'          , tamanho=[ 1, 255]   , raiz='//Nota')
    
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        
        if self.Id.valor == '':
            self.Id.valor = 'nota:' + unicode(self.NumeroNota.valor)
            
        xml += self.Id.xml
        xml += self.InscricaoMunicipalPrestador.xml
        xml += self.NumeroNota.xml
        xml += self.CodigoVerificacao.xml
        xml += '</Nota>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Id.xml = arquivo
            self.InscricaoMunicipalPrestador.xml = arquivo
            self.NumeroNota.xml = arquivo
            self.CodigoVerificacao.xml = arquivo

    xml = property(get_xml, set_xml)


class _Lote(XMLNFe):
    def __init__(self):
        super(_Lote, self).__init__()
        self.Id = TagCaracter(nome='Lote', propriedade=u'Id', raiz=u'//nfse:ReqConsultaNFSeRPS')
        self.NotaConsulta = []
        self.RPSConsulta  = []
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.Id.xml
        
        if len(self.NotaConsulta):
            xml += '<NotaConsulta>'
            
            for n in self.NotaConsulta:
                xml += n.xml
            
            xml += '</NotaConsulta>'
            
        if len(self.RPSConsulta):
            xml += '<RPSConsulta>'
        
            for r in self.RPSConsulta:
                xml += r.xml
            
            xml += '</RPSConsulta>'
            
        xml += '</Lote>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Id.xml        = arquivo
            
            notas = self._le_nohs('//nfse:ReqConsultaNFSeRPS/Lote/NotaConsulta/Nota')
            self.NotaConsulta = []
            if notas is not None:
                self.NotaConsulta = [NotaConsulta() for n in notas]
                for i in range(len(notas)):
                    self.NotaConsulta[i].xml = notas[i]

            rps = self._le_nohs('//nfse:ReqConsultaNFSeRPS/Lote/RPSConsulta/RPS')
            self.RPSConsulta = []
            if rps is not None:
                self.RPSConsulta = [RPSConsulta() for r in rps]
                for i in range(len(rps)):
                    self.RPSConsulta[i].xml = rps[i]

    xml = property(get_xml, set_xml)
    

class _Cabecalho(XMLNFe):
    def __init__(self):
        super(_Cabecalho, self).__init__()
        self.CodCidade        = TagInteiro(nome='CodCidade'        , tamanho=[ 1, 10, 1], raiz='//nfse:ReqConsultaNFSeRPS/Cabecalho')
        self.CPFCNPJRemetente = TagCaracter(nome='CPFCNPJRemetente', tamanho=[11, 14]   , raiz='//nfse:ReqConsultaNFSeRPS/Cabecalho')
        self.transacao        = TagBoolean(nome='transacao'        ,                      raiz='//nfse:ReqConsultaNFSeRPS/Cabecalho', valor=True)
        self.Versao           = TagInteiro(nome='Versao'           , tamanho=[ 1,  3, 1], raiz='//nfse:ReqConsultaNFSeRPS/Cabecalho', valor=1)
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += '<Cabecalho>'
        xml += self.CodCidade.xml
        xml += self.CPFCNPJRemetente.xml
        xml += self.transacao.xml
        xml += self.Versao.xml
        xml += '</Cabecalho>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.CodCidade.xml        = arquivo
            self.CPFCNPJRemetente.xml = arquivo
            self.transacao.xml        = arquivo
            self.Versao.xml           = arquivo

    xml = property(get_xml, set_xml)


class ReqConsultaNFSeRPS(XMLNFe):
    def __init__(self):
        super(ReqConsultaNFSeRPS, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, 'schema/', ESQUEMA_ATUAL + '/')
        self.arquivo_esquema = 'ReqConsultaNFSeRPS.xsd'
        self.Cabecalho = _Cabecalho()
        self.Lote = _Lote()
        self.Signature = Signature()

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += '<nfse:ReqConsultaNFSeRPS xmlns:nfse="http://localhost:8080/WsNFe2/lote">'
        xml += self.Cabecalho.xml
        xml += self.Lote.xml
        
        #
        # Define a URI a ser assinada
        #
        self.Signature.URI = '#' + self.Lote.Id.valor

        xml += self.Signature.xml
        
        xml += '</nfse:ReqConsultaNFSeRPS>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.Cabecalho.xml = arquivo
            self.Lote.xml = arquivo
            self.Signature.xml = self._le_noh('//nfse:ReqConsultaNFSeRPS/sig:Signature')

    xml = property(get_xml, set_xml)