#!/usr/bin/env python3
'''
Created on 20211201
Update on 20211201
@author: Eduardo Pagotto
 '''

from blockchain import Blockchain, Transactions

if __name__ == '__main__':

    # Instacia estrutura do BlockChain criando um block sem dados e adicionando com genesis 
    blockchain = Blockchain(Transactions(),dificuldade=5, coinbase={'name': 'eduardo', 'amount':1000})

    # Adiciona novas transacoes
    t1 = Transactions()
    t1.add("eduardo", 'jady',100)
    t1.add("jady", 'Hilda',10)
    t1.add("eduardo", 'josy',50)

    # Cria novo block
    blockchain.create(t1)

    # limpa transacoes e cria novo bloco
    t2 = Transactions()
    t2.add("jady", 'jose', 5)
    t2.add("jady", 'Hilda', 15)
    t2.add("eduardo", 'josy', 10)
    blockchain.create(t2, coinbase={'name': 'jady', 'amount':500})

    # log dos dados gerados
    print('Blockchain', blockchain.chain)
    