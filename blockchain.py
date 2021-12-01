#!/usr/bin/env python3
'''
Created on 20211201
Update on 20211201
@author: Eduardo Pagotto
 '''

import hashlib
import json
from time import time
from typing import List, Optional


def calc_hash(block: dict)->str:
    """ Calcula o hash do dict passado
    Args:
        block (dict): [estrutura a ser processada]
    Returns:
        str: [valor do hash]
    """

    string_object = json.dumps(block, sort_keys=True)
    block_string = string_object.encode()

    raw_hash = hashlib.sha256(block_string)
    hex_hash = raw_hash.hexdigest()

    return hex_hash

class Transactions(object):
    """ Classe de conjunto de transacoes
    Args:
        object ([type]): [description]
    """

    def __init__(self) -> None:
        super().__init__()
        self.tx : List[dict] = []

    def add(self, sender: str, recipient: str, amount: int) -> int:
        """ Adiciona uma nova transacao
        Args:
            sender (str): [from]
            recipient (str): [to]
            amount (int): [valor]
        Returns:
            int: [total de transacoes]
        """

        transaction = {'from': sender,
                       'to': recipient,
                       'amount':amount}
        self.tx.append(transaction)
        return len(self.tx)

    def clean(self):
        """ Limpa as transacoes
        """
        self.tx = []


class Blockchain(object):
    """ Classe de controle dos dados centralizados
    Args:
        object ([type]): [description]
    """

    def __init__(self, trans: Transactions, dificuldade = 3, coinbase:Optional[dict] =None) -> None:
        """ Constructor da estrutura de controle de Blockchain, transacao passada e limpa
        Args:
            trans (Transactions): [Transacao inicial]
            dificuldade (int, optional): [nivel de dificuuldade de geracao de hash]. Defaults to 3.
            coinbase (Optional[dict], optional): [Dados de CoinBase da mineracao]. Defaults to None.
        """

        super().__init__()
        self.dificuldade = dificuldade
        self.chain : List[dict] = []
        self.tx_index_master = 0
        self.create(trans, coinbase) # block genesis

    def create(self, trans: Transactions, coinbase:Optional[dict] = None) -> dict:
        """Cria o bloco, processando o hash's
        Args:
            trans (Transactions): [Dados de transacao]
            coinbase (Optional[dict], optional): [Dados de CoinBase da mineracao]. Defaults to None.

        Returns:
            dict: [bloco criado]
        """

        # se genesis inicia com zeros o hash e altura 1
        nonce = 0
        prev_block = self.chain[-1]['hash'] if len(self.chain) > 0 else '0000000000000000000000000000000000000000000000000000000000000000'

        for t in trans.tx:
            self.tx_index_master += 1
            t['tx_index'] = self.tx_index_master

        block ={'height': len(self.chain) + 1,
                'nonce': nonce,
                'time': time(),
                'tx':trans.tx, # transacoes existentes
                'n_tx': len(trans.tx),
                'prev_block': prev_block}

        # se há coinbase o adiciona ao bloco
        if coinbase is not None:
            block['coinbase'] = coinbase

        # encontra nonce que satisfaça o hash de dificuldade apropriada !!!
        while True:
            new_hash = calc_hash(block)
            base = new_hash[:self.dificuldade] 
            if set(base) == set('0'): # se (todos 0)
                block['hash'] = new_hash
                break
            else:
                nonce += 1
                block['nonce'] = nonce

        # vincula ao blocos
        self.chain.append(block)
        trans.clean()
        return block

    @property
    def last_block(self)-> dict:
        """Dict com ultimo bloco inserido
        Returns:
            dict: [bloco mais alto]
        """
        return self.chain[-1]

