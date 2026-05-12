import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

# To convert the months to their numerical representation
MONTH_MAP = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3,
    "May": 4, "June": 5, "Jul": 6, "Aug": 7,
    "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
}


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def transform(row):
    """
    Function generates the row values with all the correct types

    Args:
        row: All the values for a given row 
    """

    return [
        int(row[0]), 
        float(row[1]), 
        int(row[2]),
        float(row[3]),
        int(row[4]),
        float(row[5]),
        float(row[6]),
        float(row[7]),
        float(row[8]),
        float(row[9]),
        int(MONTH_MAP[row[10]]),  # MONTHS
        int(row[11]),
        int(row[12]),
        int(row[13]),
        int(row[14]),
        int(1 if row[15] == "Returning_Visitor" else 0),
        int(1 if bool(row[16]) else 0)
    ]


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    features = []
    labels = []
    with open(filename, mode="r") as file:
        data = csv.reader(file)

        # Skip the first row with column names
        next(data)
        for row in data:
            # Python unpacking, the last value of the row will get assigned to labels
            # and the rest will get assigned to features
            *feats, label = row
            features.append(transform(feats))
            labels.append(1 if bool(label) else 0)

    return [features, labels]


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(n_neighbors=1)
    return classifier.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_positive = 0
    correct_negative = 0

    total_positive = labels.count(1)
    total_negative = labels.count(0)

    for real, pred in zip(labels, predictions):
        # Boolean is a subclass of int, so we can add it
        correct_positive += real == pred == 1
        correct_negative += real == pred == 0

    return (correct_positive/total_positive, correct_negative/total_negative)


if __name__ == "__main__":
    main()
