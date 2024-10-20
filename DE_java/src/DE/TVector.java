package DE;



public class TVector {
    private double[] fVector;
    private int fDimension;

    public TVector(int dimension) {
        fVector = new double [dimension];
        fDimension = dimension;
    }

    public TVector(TVector vec) {
        this.copyFrom(vec);
    }

    public TVector clone() {
        return new TVector (this);
    }

    public void copyFrom(TVector vec) {
        for (int i = 0; i < fDimension;i++) {
            fVector[i] = vec.fVector[i];
        }
        fDimension = vec.fDimension;
    }

    public String toString() {
        String str = "次元数" + fDimension + "\n[";
        for (int i = 0; i < fDimension; i++) {
            str += fVector[i];
            if (i == fDimension -1) {
                str += "]\n";
            } else {
                str += ",";
            }
        }
        return str;
    }

    public void add(TVector vec) {
        for (int i = 0; i < fDimension; i++) {
            fVector[i] += vec.fVector[i];
        }
    }

    public void add(TVector vec1, TVector vec2) {
        for (int i = 0; i < fDimension; i++) {
            fVector[i] = vec1.fVector[i] + vec2.fVector[i];
        }
    }

    public void add(double value) {
        for (int i = 0; i < fDimension; i++) {
            fVector[i] += value;
        }
    }

    public void sub(TVector vec) {
        for (int i = 0; i < fDimension; i++) {
            fVector[i] -= vec.fVector[i];
        }
    }

    public void sub(TVector vec1, TVector vec2) {
        for (int i = 0; i < fDimension; i++) {
            fVector[i] = vec1.fVector[i] - vec2.fVector[i];
        }
    } 
    
    public void times(double value) {
        for (int i = 0; i < fDimension;i++) {
            fVector[i] *= value;
        }
    }

    public void fill(double value) {
        for(int i = 0;i < fDimension;i++) {
            fVector[i] = value;
        }
    }

    public double[] getArray() {
        return fVector;
    }

    public int getDimension() {
        return fDimension;
    }

    public void setValue(int index, double value) {
        fVector[index] = value;
    }

    public static void main(String[] args) {
        TVector vec = new TVector(10);
        System.out.println(vec.toString());
    }
}
