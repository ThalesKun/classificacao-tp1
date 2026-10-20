import java.util.ArrayList;

public class Ordenadores {

    // 1. bubble sort
    public static <T extends Comparable<T>> void bubbleSort(T[] vetor) {
        int n = vetor.length;

        for (int i = 0; i < n - 1; i++) {
            boolean trocou = false;

            // compara os vizinhos e leva o maior para o final
            for (int j = 0; j < n - 1 - i; j++) {
                if (vetor[j].compareTo(vetor[j + 1]) > 0) {
                    T auxiliar = vetor[j];
                    vetor[j] = vetor[j + 1];
                    vetor[j + 1] = auxiliar;
                    trocou = true;
                }
            }

            // para se não houver mais trocas
            if (trocou == false) {
                break;
            }
        }
    }

    // 2. insertion sort
    public static <T extends Comparable<T>> void insertionSort(T[] vetor) {
        for (int i = 1; i < vetor.length; i++) {
            T atual = vetor[i];
            int j = i - 1;

            // desloca os maiores para a direita
            while (j >= 0 && vetor[j].compareTo(atual) > 0) {
                vetor[j + 1] = vetor[j];
                j--;
            }

            vetor[j + 1] = atual;
        }
    }

    // 3. selection sort
    public static <T extends Comparable<T>> void selectionSort(T[] vetor) {
        for (int i = 0; i < vetor.length - 1; i++) {
            int posicaoMenor = i;

            // procura o menor na parte não ordenada
            for (int j = i + 1; j < vetor.length; j++) {
                if (vetor[j].compareTo(vetor[posicaoMenor]) < 0) {
                    posicaoMenor = j;
                }
            }

            // coloca o menor na posição atual
            T auxiliar = vetor[i];
            vetor[i] = vetor[posicaoMenor];
            vetor[posicaoMenor] = auxiliar;
        }
    }

    // 4. shell sort
    public static <T extends Comparable<T>> void shellSort(T[] vetor) {
        int n = vetor.length;
        int gap = 1;

        // gera gaps: 1, 4, 13, 40, 121...
        while (gap < n / 3) {
            gap = gap * 3 + 1;
        }

        // começa pelo maior gap e termina em 1
        while (gap > 0) {
            for (int i = gap; i < n; i++) {
                T atual = vetor[i];
                int j = i;

                // compara elementos separados pelo gap
                while (j >= gap && vetor[j - gap].compareTo(atual) > 0) {
                    vetor[j] = vetor[j - gap];
                    j = j - gap;
                }

                vetor[j] = atual;
            }

            gap = (gap - 1) / 3;
        }
    }

    // 5. heap sort
    public static <T extends Comparable<T>> void heapSort(T[] vetor) {
        int n = vetor.length;

        // organiza o vetor como um heap máximo
        for (int i = n / 2 - 1; i >= 0; i--) {
            ajustarHeap(vetor, n, i);
        }

        // coloca o maior elemento no final
        for (int fim = n - 1; fim > 0; fim--) {
            T auxiliar = vetor[0];
            vetor[0] = vetor[fim];
            vetor[fim] = auxiliar;

            ajustarHeap(vetor, fim, 0);
        }
    }

    private static <T extends Comparable<T>> void ajustarHeap(T[] vetor, int tamanho, int pai) {
        int maior = pai;
        int filhoEsquerdo = 2 * pai + 1;
        int filhoDireito = 2 * pai + 2;

        // verifica se o filho esquerdo é maior
        if (filhoEsquerdo < tamanho) {
            if (vetor[filhoEsquerdo].compareTo(vetor[maior]) > 0) {
                maior = filhoEsquerdo;
            }
        }

        // verifica se o filho direito é maior
        if (filhoDireito < tamanho) {
            if (vetor[filhoDireito].compareTo(vetor[maior]) > 0) {
                maior = filhoDireito;
            }
        }

        if (maior != pai) {
            T auxiliar = vetor[pai];
            vetor[pai] = vetor[maior];
            vetor[maior] = auxiliar;

            // verifica novamente a parte que mudou
            ajustarHeap(vetor, tamanho, maior);
        }
    }

    // 6. merge sort
    public static <T extends Comparable<T>> void mergeSort(T[] vetor) {
        if (vetor.length < 2) {
            return;
        }

        T[] auxiliar = vetor.clone();
        dividirMerge(vetor, auxiliar, 0, vetor.length - 1);
    }

    private static <T extends Comparable<T>> void dividirMerge(T[] vetor, T[] auxiliar,
                                                               int inicio, int fim) {
        if (inicio >= fim) {
            return;
        }

        // divide o vetor em duas metades
        int meio = inicio + (fim - inicio) / 2;
        dividirMerge(vetor, auxiliar, inicio, meio);
        dividirMerge(vetor, auxiliar, meio + 1, fim);

        juntarMerge(vetor, auxiliar, inicio, meio, fim);
    }

    private static <T extends Comparable<T>> void juntarMerge(T[] vetor, T[] auxiliar,
                                                              int inicio, int meio, int fim) {
        int esquerda = inicio;
        int direita = meio + 1;
        int posicao = inicio;

        // escolhe o menor elemento entre as duas metades
        while (esquerda <= meio && direita <= fim) {
            if (vetor[esquerda].compareTo(vetor[direita]) <= 0) {
                auxiliar[posicao] = vetor[esquerda];
                esquerda++;
            } else {
                auxiliar[posicao] = vetor[direita];
                direita++;
            }
            posicao++;
        }

        // copia os elementos que sobraram na esquerda
        while (esquerda <= meio) {
            auxiliar[posicao] = vetor[esquerda];
            esquerda++;
            posicao++;
        }

        // copia os elementos que sobraram na direita
        while (direita <= fim) {
            auxiliar[posicao] = vetor[direita];
            direita++;
            posicao++;
        }

        // devolve o trecho ordenado ao vetor original
        for (int i = inicio; i <= fim; i++) {
            vetor[i] = auxiliar[i];
        }
    }

    // 7. quick sort
    public static <T extends Comparable<T>> void quickSort(T[] vetor) {
        if (vetor.length < 2) {
            return;
        }

        dividirQuick(vetor, 0, vetor.length - 1);
    }

    private static <T extends Comparable<T>> void dividirQuick(T[] vetor, int inicio, int fim) {
        int esquerda = inicio;
        int direita = fim;
        T pivo = vetor[inicio + (fim - inicio) / 2];

        // separa menores e maiores em relação ao pivô
        while (esquerda <= direita) {
            while (vetor[esquerda].compareTo(pivo) < 0) {
                esquerda++;
            }

            while (vetor[direita].compareTo(pivo) > 0) {
                direita--;
            }

            if (esquerda <= direita) {
                T auxiliar = vetor[esquerda];
                vetor[esquerda] = vetor[direita];
                vetor[direita] = auxiliar;

                esquerda++;
                direita--;
            }
        }

        // ordena as partes que restaram
        if (inicio < direita) {
            dividirQuick(vetor, inicio, direita);
        }

        if (esquerda < fim) {
            dividirQuick(vetor, esquerda, fim);
        }
    }

    // 8. counting sort: somente inteiros não negativos
    public static void countingSort(int[] vetor) {
        if (vetor.length == 0) {
            return;
        }

        int maior = maiorValor(vetor);
        int[] contagem = new int[maior + 1];

        // conta quantas vezes cada número aparece
        for (int i = 0; i < vetor.length; i++) {
            int numero = vetor[i];
            contagem[numero]++;
        }

        // soma as contagens para encontrar as posições
        for (int i = 1; i < contagem.length; i++) {
            contagem[i] = contagem[i] + contagem[i - 1];
        }

        int[] ordenado = new int[vetor.length];

        // coloca os números na posição correta, de trás para frente
        for (int i = vetor.length - 1; i >= 0; i--) {
            int numero = vetor[i];
            int posicao = contagem[numero] - 1;
            ordenado[posicao] = numero;
            contagem[numero]--;
        }

        for (int i = 0; i < vetor.length; i++) {
            vetor[i] = ordenado[i];
        }
    }

    // 9. radix sort: somente inteiros não negativos
    public static void radixSort(int[] vetor) {
        if (vetor.length == 0) {
            return;
        }

        int maior = maiorValor(vetor);
        int[] auxiliar = new int[vetor.length];

        // passa pelas unidades, dezenas, centenas...
        for (long casa = 1; maior / casa > 0; casa = casa * 10) {
            int[] contagem = new int[10];

            // conta os dígitos da casa atual
            for (int i = 0; i < vetor.length; i++) {
                int digito = (int) ((vetor[i] / casa) % 10);
                contagem[digito]++;
            }

            // soma as contagens para descobrir as posições
            for (int i = 1; i < 10; i++) {
                contagem[i] = contagem[i] + contagem[i - 1];
            }

            // organiza os números pela casa atual
            for (int i = vetor.length - 1; i >= 0; i--) {
                int numero = vetor[i];
                int digito = (int) ((numero / casa) % 10);
                int posicao = contagem[digito] - 1;

                auxiliar[posicao] = numero;
                contagem[digito]--;
            }

            for (int i = 0; i < vetor.length; i++) {
                vetor[i] = auxiliar[i];
            }
        }
    }

    // 10. bucket sort: somente inteiros não negativos
    public static void bucketSort(int[] vetor) {
        if (vetor.length == 0) {
            return;
        }

        int maior = maiorValor(vetor);
        int quantidadeBaldes = vetor.length;
        long largura = (long) maior / quantidadeBaldes + 1;

        // cria os baldes vazios
        ArrayList<ArrayList<Integer>> baldes = new ArrayList<>();
        for (int i = 0; i < quantidadeBaldes; i++) {
            baldes.add(new ArrayList<Integer>());
        }

        // distribui os números pelos intervalos
        for (int i = 0; i < vetor.length; i++) {
            int numero = vetor[i];
            int indiceBalde = (int) (numero / largura);
            baldes.get(indiceBalde).add(numero);
        }

        int posicaoVetor = 0;
        for (int b = 0; b < baldes.size(); b++) {
            ArrayList<Integer> balde = baldes.get(b);

            // ordena cada balde com insertion sort
            for (int i = 1; i < balde.size(); i++) {
                int atual = balde.get(i);
                int j = i - 1;

                while (j >= 0 && balde.get(j) > atual) {
                    balde.set(j + 1, balde.get(j));
                    j--;
                }

                balde.set(j + 1, atual);
            }

            // devolve os números ao vetor original
            for (int i = 0; i < balde.size(); i++) {
                vetor[posicaoVetor] = balde.get(i);
                posicaoVetor++;
            }
        }
    }

    // usado por counting, radix e bucket
    private static int maiorValor(int[] vetor) {
        int maior = 0;

        for (int i = 0; i < vetor.length; i++) {
            if (vetor[i] < 0) {
                throw new IllegalArgumentException("Use somente números não negativos.");
            }

            if (vetor[i] > maior) {
                maior = vetor[i];
            }
        }

        return maior;
    }
}
