import static org.junit.Assert.*;
import org.junit.Test;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class CalculadoraLLMTest {

    private String rodarCalculadora(String input) {
        // Simula a entrada do usuário
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        System.setIn(in);

        // Captura a saída do console
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));

        // Executa a calculadora
        CalculadoraSimples.main(new String[0]);

        return out.toString();
    }

    @Test
    public void testSoma() {
        String output = rodarCalculadora("+\n10\n5\n");
        assertTrue("Soma falhou", output.contains("Resultado: 15.0"));
    }

    @Test
    public void testDivisaoPorZero() {
        String output = rodarCalculadora("/\n10\n0\n");
        assertTrue("Validação de zero falhou", output.contains("Erro: Não é possível dividir por zero!"));
    }

    @Test
    public void testOperacaoInvalida() {
        String output = rodarCalculadora("?\n1\n1\n");
        assertTrue("Falha na operação inválida", output.contains("Operação inválida."));
    }
}