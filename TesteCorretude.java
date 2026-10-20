import java.util.Arrays;
import java.util.Random;

/**
 * Etapa 1 do TP1 - Verificacao de corretude dos algoritmos de ordenacao.
 *
 * Testa os 10 algoritmos de Ordenadores.java com vetores pequenos (10-15 elementos),
 * cobrindo: ordem crescente, decrescente, aleatoria e com repeticoes,
 * em tamanhos par e impar.
 *
 * Nao mede desempenho - serve apenas para checar se as implementacoes estao corretas
 * antes de partir para os experimentos de desempenho (Etapa 2 em diante).
 */
public class TesteCorretude {

    private static int totalTestes = 0;
    private static int testesOk = 0;

    public static void main(String[] args) {
        System.out.println("=== Verificacao de corretude - TP1 ACD ===\n");

        // --- Casos de teste para os algoritmos baseados em COMPARACAO (Integer[]) ---
        // tamanho par (12) e impar (13), cobrindo os 4 casos pedidos no enunciado

        testarCaso("Crescente (par, 12)", gerarCrescente(12));
        testarCaso("Decrescente (par, 12)", gerarDecrescente(12));
        testarCaso("Aleatorio (par, 12)", gerarAleatorio(12, 42));
        testarCaso("Com repeticoes (par, 12)", gerarComRepeticoes(12, 42));

        testarCaso("Crescente (impar, 13)", gerarCrescente(13));
        testarCaso("Decrescente (impar, 13)", gerarDecrescente(13));
        testarCaso("Aleatorio (impar, 13)", gerarAleatorio(13, 7));
        testarCaso("Com repeticoes (impar, 13)", gerarComRepeticoes(13, 7));

        // tamanho extra so para ampliar a cobertura (15 elementos)
        testarCaso("Aleatorio (15)", gerarAleatorio(15, 99));

        // --- Casos de teste para os algoritmos LINEARES (int[], somente nao negativos) ---
        testarCasoLinear("Linear - Crescente (par, 12)", gerarCrescenteInt(12));
        testarCasoLinear("Linear - Decrescente (par, 12)", gerarDecrescenteInt(12));
        testarCasoLinear("Linear - Aleatorio (par, 12)", gerarAleatorioInt(12, 42));
        testarCasoLinear("Linear - Com repeticoes (par, 12)", gerarComRepeticoesInt(12, 42));

        testarCasoLinear("Linear - Crescente (impar, 13)", gerarCrescenteInt(13));
        testarCasoLinear("Linear - Decrescente (impar, 13)", gerarDecrescenteInt(13));
        testarCasoLinear("Linear - Aleatorio (impar, 13)", gerarAleatorioInt(13, 7));
        testarCasoLinear("Linear - Com repeticoes (impar, 13)", gerarComRepeticoesInt(13, 7));

        System.out.println("\n=== Resultado final: " + testesOk + "/" + totalTestes + " testes OK ===");
        if (testesOk != totalTestes) {
            System.out.println(">>> ATENCAO: existem falhas. Revise os algoritmos indicados acima.");
        } else {
            System.out.println(">>> Todos os algoritmos passaram na verificacao de corretude.");
        }
    }

    // ---------------------------------------------------------------
    // Execucao dos testes - algoritmos de comparacao (Integer[])
    // ---------------------------------------------------------------
    private static void testarCaso(String nomeCaso, Integer[] vetorOriginal) {
        System.out.println("--- Caso: " + nomeCaso + " ---");
        System.out.println("Entrada: " + Arrays.toString(vetorOriginal));

        Integer[] esperado = vetorOriginal.clone();
        Arrays.sort(esperado); // usado so como gabarito nesta etapa de verificacao

        verificar("bubbleSort", nomeCaso, () -> {
            Integer[] copia = vetorOriginal.clone();
            Ordenadores.bubbleSort(copia);
            return copia;
        }, esperado);

        verificar("insertionSort", nomeCaso, () -> {
            Integer[] copia = vetorOriginal.clone();
            Ordenadores.insertionSort(copia);
            return copia;
        }, esperado);

        verificar("selectionSort", nomeCaso, () -> {
            Integer[] copia = vetorOriginal.clone();
            Ordenadores.selectionSort(copia);
            return copia;
        }, esperado);

        verificar("shellSort", nomeCaso, () -> {
            Integer[] copia = vetorOriginal.clone();
            Ordenadores.shellSort(copia);
            return copia;
        }, esperado);

        verificar("heapSort", nomeCaso, () -> {
            Integer[] copia = vetorOriginal.clone();
            Ordenadores.heapSort(copia);
            return copia;
        }, esperado);

        verificar("mergeSort", nomeCaso, () -> {
            Integer[] copia = vetorOriginal.clone();
            Ordenadores.mergeSort(copia);
            return copia;
        }, esperado);

        verificar("quickSort", nomeCaso, () -> {
            Integer[] copia = vetorOriginal.clone();
            Ordenadores.quickSort(copia);
            return copia;
        }, esperado);

        System.out.println();
    }

    // ---------------------------------------------------------------
    // Execucao dos testes - algoritmos lineares (int[])
    // ---------------------------------------------------------------
    private static void testarCasoLinear(String nomeCaso, int[] vetorOriginal) {
        System.out.println("--- Caso: " + nomeCaso + " ---");
        System.out.println("Entrada: " + Arrays.toString(vetorOriginal));

        int[] esperado = vetorOriginal.clone();
        Arrays.sort(esperado);

        verificarLinear("countingSort", nomeCaso, vetorOriginal, Ordenadores::countingSort, esperado);
        verificarLinear("radixSort", nomeCaso, vetorOriginal, Ordenadores::radixSort, esperado);
        verificarLinear("bucketSort", nomeCaso, vetorOriginal, Ordenadores::bucketSort, esperado);

        System.out.println();
    }

    @FunctionalInterface
    private interface Ordenador {
        Integer[] ordenar();
    }

    @FunctionalInterface
    private interface OrdenadorLinear {
        void ordenar(int[] vetor);
    }

    private static void verificar(String nomeAlgoritmo, String nomeCaso, Ordenador acao, Integer[] esperado) {
        totalTestes++;
        try {
            Integer[] resultado = acao.ordenar();
            if (Arrays.equals(resultado, esperado)) {
                System.out.println("  [OK] " + nomeAlgoritmo);
                testesOk++;
            } else {
                System.out.println("  [FALHOU] " + nomeAlgoritmo
                        + " | esperado=" + Arrays.toString(esperado)
                        + " | obtido=" + Arrays.toString(resultado));
            }
        } catch (Exception e) {
            System.out.println("  [ERRO] " + nomeAlgoritmo + " lancou excecao: " + e);
        }
    }

    private static void verificarLinear(String nomeAlgoritmo, String nomeCaso, int[] entrada,
                                         OrdenadorLinear acao, int[] esperado) {
        totalTestes++;
        try {
            int[] copia = entrada.clone();
            acao.ordenar(copia);
            if (Arrays.equals(copia, esperado)) {
                System.out.println("  [OK] " + nomeAlgoritmo);
                testesOk++;
            } else {
                System.out.println("  [FALHOU] " + nomeAlgoritmo
                        + " | esperado=" + Arrays.toString(esperado)
                        + " | obtido=" + Arrays.toString(copia));
            }
        } catch (Exception e) {
            System.out.println("  [ERRO] " + nomeAlgoritmo + " lancou excecao: " + e);
        }
    }

    // ---------------------------------------------------------------
    // Geradores de vetores de teste - versao Integer[] (algoritmos de comparacao)
    // ---------------------------------------------------------------
    private static Integer[] gerarCrescente(int n) {
        Integer[] vetor = new Integer[n];
        for (int i = 0; i < n; i++) vetor[i] = i + 1;
        return vetor;
    }

    private static Integer[] gerarDecrescente(int n) {
        Integer[] vetor = new Integer[n];
        for (int i = 0; i < n; i++) vetor[i] = n - i;
        return vetor;
    }

    private static Integer[] gerarAleatorio(int n, long seed) {
        Random rand = new Random(seed);
        Integer[] vetor = new Integer[n];
        for (int i = 0; i < n; i++) vetor[i] = rand.nextInt(100);
        return vetor;
    }

    private static Integer[] gerarComRepeticoes(int n, long seed) {
        Random rand = new Random(seed);
        Integer[] vetor = new Integer[n];
        // poucos valores possiveis para forcar repeticoes
        for (int i = 0; i < n; i++) vetor[i] = rand.nextInt(4);
        return vetor;
    }

    // ---------------------------------------------------------------
    // Geradores de vetores de teste - versao int[] (algoritmos lineares, nao negativos)
    // ---------------------------------------------------------------
    private static int[] gerarCrescenteInt(int n) {
        int[] vetor = new int[n];
        for (int i = 0; i < n; i++) vetor[i] = i + 1;
        return vetor;
    }

    private static int[] gerarDecrescenteInt(int n) {
        int[] vetor = new int[n];
        for (int i = 0; i < n; i++) vetor[i] = n - i;
        return vetor;
    }

    private static int[] gerarAleatorioInt(int n, long seed) {
        Random rand = new Random(seed);
        int[] vetor = new int[n];
        for (int i = 0; i < n; i++) vetor[i] = rand.nextInt(100);
        return vetor;
    }

    private static int[] gerarComRepeticoesInt(int n, long seed) {
        Random rand = new Random(seed);
        int[] vetor = new int[n];
        for (int i = 0; i < n; i++) vetor[i] = rand.nextInt(4);
        return vetor;
    }
}
