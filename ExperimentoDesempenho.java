import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

/**
 * Etapas 2, 3 e 4 do TP1 - Medicao de desempenho dos algoritmos de ordenacao.
 *
 * - Gera vetores de diferentes tamanhos e ordens (crescente, decrescente, aleatorio)
 * - Garante que todos os algoritmos de uma mesma configuracao recebem os MESMOS dados
 *   (copia por execucao, conforme item 2.3 do enunciado)
 * - Mede apenas o tempo de ordenacao com System.nanoTime(), com warm-up previo da JVM
 * - Executa N repeticoes por configuracao e grava TODOS os tempos individuais em CSV
 *
 * Saida: resultados.csv (algoritmo, tamanho, ordenacao, repeticao, tempo_ns)
 */
public class ExperimentoDesempenho {

    // ---------------------------------------------------------------
    // CONFIGURACAO DO EXPERIMENTO - ajuste aqui se precisar
    // ---------------------------------------------------------------
    private static final int[] TAMANHOS = {1_000, 10_000};
    private static final String[] ORDENACOES = {"crescente", "decrescente", "aleatorio"};
    private static final int REPETICOES_WARMUP = 3; // execucoes de aquecimento da JVM, descartadas
    private static final long SEED_BASE = 20261020L; // fixa para reprodutibilidade

    // Combinacoes "algoritmo:tamanho" a pular (ex.: "bubbleSort:1000000").
    // Util se uma combinacao O(n^2) em 1.000.000 estiver demorando demais.
    private static final Set<String> PULAR = new HashSet<>();
    // Exemplo: descomente se precisar
    // static { PULAR.add("bubbleSort:1000000"); PULAR.add("selectionSort:1000000"); }

    private static BufferedWriter csv;

    public static void main(String[] args) throws IOException {
        csv = new BufferedWriter(new FileWriter("resultados.csv"));
        csv.write("algoritmo,tamanho,ordenacao,repeticao,tempo_ns\n");
        csv.flush();

        for (int tamanho : TAMANHOS) {
            for (String ordenacao : ORDENACOES) {
                int[] base = gerarVetorBase(tamanho, ordenacao, SEED_BASE + tamanho);
                int repeticoes = repeticoesPara(tamanho);

                System.out.println("\n=== tamanho=" + tamanho + " ordenacao=" + ordenacao
                        + " repeticoes=" + repeticoes + " ===");

                // --- algoritmos baseados em comparacao (Integer[]) ---
                Integer[] baseBoxed = boxear(base);
                rodarComparacao("bubbleSort", baseBoxed, tamanho, ordenacao, repeticoes, Ordenadores::bubbleSort);
                rodarComparacao("insertionSort", baseBoxed, tamanho, ordenacao, repeticoes, Ordenadores::insertionSort);
                rodarComparacao("selectionSort", baseBoxed, tamanho, ordenacao, repeticoes, Ordenadores::selectionSort);
                rodarComparacao("shellSort", baseBoxed, tamanho, ordenacao, repeticoes, Ordenadores::shellSort);
                rodarComparacao("heapSort", baseBoxed, tamanho, ordenacao, repeticoes, Ordenadores::heapSort);
                rodarComparacao("mergeSort", baseBoxed, tamanho, ordenacao, repeticoes, Ordenadores::mergeSort);
                rodarComparacao("quickSort", baseBoxed, tamanho, ordenacao, repeticoes, Ordenadores::quickSort);

                // --- algoritmos de tempo linear (int[], somente nao negativos) ---
                rodarLinear("countingSort", base, tamanho, ordenacao, repeticoes, Ordenadores::countingSort);
                rodarLinear("radixSort", base, tamanho, ordenacao, repeticoes, Ordenadores::radixSort);
                rodarLinear("bucketSort", base, tamanho, ordenacao, repeticoes, Ordenadores::bucketSort);
            }
        }

        csv.close();
        System.out.println("\nConcluido. Resultados em resultados.csv");
    }

    // 30 repeticoes ate 100.000 elementos (conforme recomendado no enunciado),
    // 10 repeticoes em 1.000.000 para manter o tempo total viavel.
    private static int repeticoesPara(int tamanho) {
        return tamanho <= 100_000 ? 30 : 10;
    }

    @FunctionalInterface
    interface SortComparacao {
        void sort(Integer[] vetor);
    }

    @FunctionalInterface
    interface SortLinear {
        void sort(int[] vetor);
    }

    private static void rodarComparacao(String nome, Integer[] base, int tamanho, String ordenacao,
                                         int repeticoes, SortComparacao sort) throws IOException {
        if (PULAR.contains(nome + ":" + tamanho)) {
            System.out.println("  [pulado] " + nome);
            return;
        }

        // warm-up da JVM - nao entra nos resultados
        for (int w = 0; w < REPETICOES_WARMUP; w++) {
            Integer[] copia = base.clone();
            sort.sort(copia);
        }

        long inicioConfig = System.nanoTime();
        for (int r = 1; r <= repeticoes; r++) {
            Integer[] copia = base.clone(); // copia fica FORA da medicao
            long inicio = System.nanoTime();
            sort.sort(copia);
            long fim = System.nanoTime();
            registrar(nome, tamanho, ordenacao, r, fim - inicio);
        }
        double segundos = (System.nanoTime() - inicioConfig) / 1e9;
        System.out.printf("  %-15s %8.3f s (total, %d repeticoes)%n", nome, segundos, repeticoes);
    }

    private static void rodarLinear(String nome, int[] base, int tamanho, String ordenacao,
                                     int repeticoes, SortLinear sort) throws IOException {
        if (PULAR.contains(nome + ":" + tamanho)) {
            System.out.println("  [pulado] " + nome);
            return;
        }

        for (int w = 0; w < REPETICOES_WARMUP; w++) {
            int[] copia = base.clone();
            sort.sort(copia);
        }

        long inicioConfig = System.nanoTime();
        for (int r = 1; r <= repeticoes; r++) {
            int[] copia = base.clone();
            long inicio = System.nanoTime();
            sort.sort(copia);
            long fim = System.nanoTime();
            registrar(nome, tamanho, ordenacao, r, fim - inicio);
        }
        double segundos = (System.nanoTime() - inicioConfig) / 1e9;
        System.out.printf("  %-15s %8.3f s (total, %d repeticoes)%n", nome, segundos, repeticoes);
    }

    private static void registrar(String algoritmo, int tamanho, String ordenacao, int repeticao, long tempoNs)
            throws IOException {
        csv.write(algoritmo + "," + tamanho + "," + ordenacao + "," + repeticao + "," + tempoNs + "\n");
        csv.flush(); // garante que nada se perde se o processo for interrompido (Ctrl+C)
    }

    private static Integer[] boxear(int[] vetor) {
        Integer[] resultado = new Integer[vetor.length];
        for (int i = 0; i < vetor.length; i++) {
            resultado[i] = vetor[i];
        }
        return resultado;
    }

    // Gera o vetor BASE de uma configuracao (tamanho + ordenacao).
    // Esse mesmo vetor (via clone) e usado por TODOS os algoritmos dessa configuracao,
    // garantindo comparabilidade (item 2.3 do enunciado).
    private static int[] gerarVetorBase(int tamanho, String ordenacao, long seed) {
        int[] vetor = new int[tamanho];
        switch (ordenacao) {
            case "crescente":
                for (int i = 0; i < tamanho; i++) {
                    vetor[i] = i;
                }
                break;
            case "decrescente":
                for (int i = 0; i < tamanho; i++) {
                    vetor[i] = tamanho - i;
                }
                break;
            case "aleatorio":
                Random rand = new Random(seed);
                for (int i = 0; i < tamanho; i++) {
                    vetor[i] = rand.nextInt(tamanho * 10 + 1); // nao negativo, exigido por counting/radix/bucket
                }
                break;
            default:
                throw new IllegalArgumentException("Ordenacao desconhecida: " + ordenacao);
        }
        return vetor;
    }
}
