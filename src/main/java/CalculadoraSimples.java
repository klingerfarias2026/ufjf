import java.util.Scanner;

public class CalculadoraSimples {

    public static void main(String[] args) {
        Scanner leitor = new Scanner(System.in);

        System.out.println("--- Calculadora Java ---");
        System.out.println("Escolha a operação: (+, -, *, /)");
        char operacao = leitor.next().charAt(0);

        System.out.println("Digite o primeiro número:");
        double num1 = leitor.nextDouble();

        System.out.println("Digite o segundo número:");
        double num2 = leitor.nextDouble();

        double resultado;

        switch (operacao) {
            case '+':
                resultado = num1 + num2;
                System.out.println("Resultado: " + resultado);
                break;
            case '-':
                resultado = num1 - num2;
                System.out.println("Resultado: " + resultado);
                break;
            case '*':
                resultado = num1 * num2;
                System.out.println("Resultado: " + resultado);
                break;
            case '/':
                if (num2 != 0) {
                    resultado = num1 / num2;
                    System.out.println("Resultado: " + resultado);
                } else {
                    System.out.println("Erro: Não é possível dividir por zero!");
                }
                break;
            default:
                System.out.println("Operação inválida.");
                break;
        }

        leitor.close();
        System.out.println("------------------------");
    }
}