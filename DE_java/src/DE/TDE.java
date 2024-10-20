package DE;


import java.util.Random;

public class TDE {
    private TIndividual[] fPopulation;
    private TIndividual fBestIndividual;
    private int fPopulationSize;
    private int fDimension;
    private int fIndex1;
    private int fIndex2;
    private int fIndex3;
    private int fJRand;
    private double fMax;
    private double fMin;
    private TVector fCaluculate1;
    private TVector fCaluculate2;
    private Random fRandom;
    public static final double F = 1.0;
    public static final double CR = 0.5;

    public TDE(int dimension, int populationSize, double max, double min, Random rand) {
        fPopulationSize = populationSize;
        fPopulation = new TIndividual [fPopulationSize];
        for (int i = 0; i < fPopulationSize; i++) {
            fPopulation[i] = new TIndividual(dimension);
        }
        fBestIndividual = new TIndividual(dimension);
        fDimension = dimension;
        fIndex1 = -1;
        fIndex2 = -1;
        fIndex3 = -1;
        fJRand = -1;
        fMax = max;
        fMin = min;
        fCaluculate1 = new TVector(dimension);
        fCaluculate2 = new TVector(dimension);
        fRandom = rand;
    }

    public void initialize(IFunction function) {
        generateInitialPopulation();
        setEvaluationValueOfVector(function);
    }

    public void generateInitialPopulation() {
        for (int i = 0; i < fPopulationSize; i++) {
            TIndividual ind = fPopulation[i];
            for (int j = 0; j < fDimension; j++) {
                ind.getVector().getArray()[j] = fRandom.nextDouble();
            }
            ind.getVector().times(fMax-fMin);
            ind.getVector().add(fMin);
        }
    }

    public void setEvaluationValueOfVector(IFunction function) {
        for (int i = 0; i < fPopulationSize; i++) {
            TIndividual ind = fPopulation[i];
            double eval = function.evaluate(ind.getVector());
            ind.setEvaluationValue(eval);
        }
    }

    public void createMutationVector() {
        for (int i = 0; i < fPopulationSize; i++) {
            selectIndex(i);
            fCaluculate1.copyFrom(fPopulation[fIndex1].getVector());
            fCaluculate2.sub(fPopulation[fIndex2].getVector(), fPopulation[fIndex2].getVector());
            fCaluculate2.times(F);
            fPopulation[i].getMutationVector().add(fCaluculate1, fCaluculate2);
        }
    }

    public void selectIndex(int indexOfInd) {
        while (true) {
            fIndex1 = fRandom.nextInt(fPopulationSize);
            if (indexOfInd != fIndex1) {
                break;
            }
        }
        while (true) {
            fIndex2 = fRandom.nextInt(fPopulationSize);
            if (indexOfInd != fIndex2 && fIndex1 != fIndex2) {
                break;
            }
        }
        while (true) {
            fIndex3 = fRandom.nextInt(fPopulationSize);
            if (indexOfInd != fIndex3 && fIndex1 != fIndex3 && fIndex2 != fIndex3) {
                break;
            }
        }
    }

    public void createAimVector() {
        for (int i = 0; i < fPopulationSize; i++) {
            TIndividual ind = fPopulation[i];
            fJRand = fRandom.nextInt(fDimension);
            for (int j = 0; j < fDimension; j++) {
                if (fRandom.nextDouble() <= CR || j == fJRand) {
                    ind.getAimVector().getArray()[j] = ind.getMutationVector().getArray()[j];
                } else {
                    ind.getAimVector().getArray()[j] = ind.getVector().getArray()[j];
                }
            }
        }
    }

    public void setEvaluationValueOfAimVector (IFunction function) {
        for (int i = 0; i < fPopulationSize; i++) {
            TIndividual ind = fPopulation[i];
            double eval = function.evaluate(ind.getAimVector());
            ind.setEvaluationValueOfAimVector(eval);
            //System.out.println(eval);
        }
    }

    public void selectIndividualForNextGeneration() {
        for (int i = 0; i < fPopulationSize; i++) {
            TIndividual ind = fPopulation[i];
            if (ind.comparisonEvaluationValue()) {
                ind.getVector().copyFrom(ind.getAimVector());
                ind.setEvaluationValue(ind.getEvaluationValueOfAimVector());
            }
        }
    }

    public void doOneGeneration(IFunction function) {
        createMutationVector();
        createAimVector();
        setEvaluationValueOfAimVector(function);
        selectIndividualForNextGeneration();
        getBestIndividual();
    }

    public void getBestIndividual() {
        for (int i = 0; i < fPopulationSize - 1; i++) {
            TIndividual ind = fPopulation[i];
            if (fPopulation[i + 1].getEvaluationValue() < ind.getEvaluationValue()) {
                ind = fPopulation[i + 1];
            }
            if (i == fPopulationSize - 2) {
                fBestIndividual.copyFrom(ind);
            }
        }
        System.out.println(fBestIndividual.toString());
    }

    public TIndividual getPopulation(int index) {
        return fPopulation[index];
    }
}
