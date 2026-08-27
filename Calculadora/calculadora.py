import divide
import multiplicacao
import resto
import soma
import subtrai

def testeSoma():
    assert soma.somaf(2, 3) == 5, "Erro: 2 + 3 deveria ser 5"
    assert soma.somaf(2.5, 3.7) == 6.2, "Erro: 2.5 + 3.7 deveria ser 6.2"
    assert soma.somaf(-1.5, 4.5) == 3.0, "Erro: -1.5 + 4.5 deveria ser 3.0"
    assert soma.somaf(0, 5) == 5, "Erro: 0 + 5 deveria ser 5"
    assert soma.somaf(5, 0) == 5, "Erro: 5 + 0 deveria ser 5"
    assert soma.somaf(1.1, 1.1) == 2.2, "Erro: 1.1 + 1.1 deveria ser 2.2"
    return

def testeMultiplicacao():
    assert multiplicacao.multiplicaf(2, 3) == 6, "Erro: 2 * 3 deveria ser 6"
    assert multiplicacao.multiplicaf(2.5, 3.0) == 7.5, "Erro: 2.5 * 3.0 deveria ser 7.5"
    assert multiplicacao.multiplicaf(1.5, 1.5) == 2.25, "Erro: 1.5 * 1.5 deveria ser 2.25"
    assert multiplicacao.multiplicaf(-1.5, 4.0) == -6.0, "Erro: -1.5 * 4.0 deveria ser -6.0"
    assert multiplicacao.multiplicaf(-2, -3) == 6, "Erro: -2 * -3 deveria ser 6"
    assert multiplicacao.multiplicaf(0, 5) == 0, "Erro: 0 * 5 deveria ser 0"
    assert multiplicacao.multiplicaf(5, 0) == 0, "Erro: 5 * 0 deveria ser 0"
    return

def testeResto(): 
    assert resto.restof(10, 3) == 1, "Erro: 10 % 3 deveria ser 1"
    assert resto.restof(7, 2) == 1, "Erro: 7 % 2 deveria ser 1"
    assert resto.restof(8, 4) == 0, "Erro: 8 % 4 deveria ser 0"
    assert resto.restof(3, 10) == 3, "Erro: 3 % 10 deveria ser 3"
    assert resto.restof(5.5, 2.0) == 1.5, "Erro: 5.5 % 2.0 deveria ser 1.5"
    assert resto.restof(0, 5) == 0, "Erro: 0 % 5 deveria ser 0"
    assert resto.restof(-7, 3) == 2, "Erro: -7 % 3 deveria ser 2"
    return

def testeDivide():
    assert divide.dividef(6, 3) == 2, "Erro: 6 / 3 deveria ser 2"
    assert divide.dividef(7, 2) == 3.5, "Erro: 7 / 2 deveria ser 3.5"
    assert divide.dividef(2.5, 0.5) == 5.0, "Erro: 2.5 / 0.5 deveria ser 5.0"
    assert divide.dividef(-6, 2) == -3.0, "Erro: -6 / 2 deveria ser -3.0"
    assert divide.dividef(-6, -2) == 3.0, "Erro: -6 / -2 deveria ser 3.0"
    assert divide.dividef(0, 5) == 0, "Erro: 0 / 5 deveria ser 0"
    assert divide.dividef(1, 4) == 0.25, "Erro: 1 / 4 deveria ser 0.25"
    return

def testeSubtrai():
    assert subtrai.subtraif(5, 3) == 2, "Erro: 5 - 3 deveria ser 2"
    assert subtrai.subtraif(3, 5) == -2, "Erro: 3 - 5 deveria ser -2"
    assert subtrai.subtraif(5.5, 2.3) == 3.2, "Erro: 5.5 - 2.3 deveria ser 3.2"
    assert subtrai.subtraif(-1.5, 4.5) == -6.0, "Erro: -1.5 - 4.5 deveria ser -6.0"
    assert subtrai.subtraif(-2, -3) == 1, "Erro: -2 - (-3) deveria ser 1"
    assert subtrai.subtraif(0, 5) == -5, "Erro: 0 - 5 deveria ser -5"
    assert subtrai.subtraif(5, 0) == 5, "Erro: 5 - 0 deveria ser 5"
    return
def pergunta():
    operacao = input("Qual operação você quer fazer? ")
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
 
    if operacao == "+":
        resultado = soma.somaf(num1, num2)
    elif operacao == "-":
        resultado = subtrai.subtraif(num1, num2)
    elif operacao == "*":
        resultado = multiplicacao.multiplicaf(num1, num2)
    elif operacao == "/":
        resultado = divide.dividef(num1, num2)
    elif operacao == "%":
        resultado = resto.restof(num1, num2)
    else:
        print("Operação inválida, tente novamente.")
        return
 
    print("Resultado:", resultado)

testeSoma()
testeMultiplicacao()
testeResto()
testeDivide()
testeSubtrai()
print("Todos os testes passaram com sucesso!")
pergunta()
