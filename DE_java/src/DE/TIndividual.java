package DE;



public class TIndividual {
    
    private TVector fVector;
    private TVector fMutationVector;
    private TVector fAimVector;
    private double fEvaluationValue;
    private double fEvaluationValueOfAimVector;

    public TIndividual(int dimension) {
        fVector = new TVector(dimension);
        fMutationVector = new TVector(dimension);
        fAimVector = new TVector(dimension);
        fEvaluationValue = Double.NaN;
        fEvaluationValueOfAimVector = Double.NaN;
    }

    public TIndividual(TIndividual ind) {
        copyFrom(ind);
    }

    public void copyFrom(TIndividual ind) {
        fVector.copyFrom(ind.fVector);
        fAimVector.copyFrom(ind.fAimVector);
        fMutationVector.copyFrom(ind.fMutationVector);
        fEvaluationValue = ind.fEvaluationValue;
        fEvaluationValueOfAimVector= ind.fEvaluationValueOfAimVector;
    }

    public String toString() {
        String str = "";
        str = fVector.toString();
        str += "評価値:" + fEvaluationValue;
        return str;
    }

    public boolean comparisonEvaluationValue() {
        if (fEvaluationValueOfAimVector <= fEvaluationValue) {
            return true;
        } else {
            return false;
        }
    }

    public TVector getVector() {
        return fVector;
    }

    public TVector getAimVector() {
        return fAimVector;
    }

    public TVector getMutationVector() {
        return fMutationVector;
    }

    public double getEvaluationValue() {
        return fEvaluationValue;
    }

    public double getEvaluationValueOfAimVector() {
        return fEvaluationValueOfAimVector;
    }

    public void setEvaluationValue(double eval) {
        fEvaluationValue = eval;
    }

    public void setEvaluationValueOfAimVector (double eval) {
        fEvaluationValueOfAimVector = eval;
    }
}
