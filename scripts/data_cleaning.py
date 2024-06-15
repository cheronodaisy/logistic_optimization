class OutlierHandler:
    def __init__(self, df):
        self.df = df

    def calculate_iqr(self, column):
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return lower_bound, upper_bound

    def detect_outliers(self, column):
        lower_bound, upper_bound = self.calculate_iqr(column)
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        return outliers

    def remove_outliers(self, column):
        lower_bound, upper_bound = self.calculate_iqr(column)
        self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]

    def impute_outliers(self, column):
        lower_bound, upper_bound = self.calculate_iqr(column)
        median_value = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)][column].median()
        self.df[column] = self.df[column].apply(
            lambda x: median_value if (x < lower_bound or x > upper_bound) else x
        )

    def handle_all_columns(self, method='remove'):
        numerical_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        categorical_columns = self.df.select_dtypes(include=['object']).columns

        for column in numerical_columns:
            if method == 'remove':
                self.remove_outliers(column)
            elif method == 'impute':
                self.impute_outliers(column)

        for column in categorical_columns:
            mode_value = self.df[column].mode()[0]
            self.df[column].fillna(mode_value, inplace=True)
if __name__ == "__main__":

    # Instantiate and apply OutlierHandler
    handler = OutlierHandler(df)
    handler.handle_all_columns(method='impute')