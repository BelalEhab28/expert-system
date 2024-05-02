import streamlit as st
from experta import Rule, Fact, KnowledgeEngine,AND , OR ,P





# Define classes for facts
class Name(Fact):
    pass


class Age(Fact):
    pass


class Weight(Fact):
    pass


class Height(Fact):
    pass


class Gender(Fact):
    pass


class Lifestyle(Fact):
    pass


# Define the Expert System rules
class HealthExpert(KnowledgeEngine):
    @Rule(
        OR(
            AND(
                Weight(status="overweight"),
                Gender(gender="Male"),
                Age(age=P(lambda x: isinstance(x, int))),
                Lifestyle(lifestyle=P(lambda x: isinstance(x, str)))
            ),
            AND(
                Weight(status="overweight"),
                Gender(gender="Female"),
                Age(age=P(lambda x: isinstance(x, int))),
                Lifestyle(lifestyle=P(lambda x: isinstance(x, str)))
            ),
            AND(
                Weight(status="underweight"),
                Age(age=P(lambda x: isinstance(x, int))),
                Lifestyle(lifestyle=P(lambda x: isinstance(x, str)))
            ),
            AND(
                Height(height=P(lambda x: isinstance(x, int))),
                Weight(status="good")
            )
        )
    )
    def calculate_calories(self):
        weight = self.weight
        height = self.height
        age = self.age
        lifestyle = self.lifestyle
        gender = self.gender

        bmr = 0
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == "Female":
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        activity_factor = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725
        }

        tdee = bmr * activity_factor[lifestyle]

        if weight >= 18.5 and weight <= 24.9:
            st.write("Your weight is good.")
        elif weight < 18.5:
            st.write("You are underweight.")
        else:
            st.write("You are overweight.")

        st.write("Your Total Daily Energy Expenditure (TDEE) is:", round(tdee, 2), "calories.")


# Streamlit GUI
def main():
    st.title("Health Expert System")

    name = st.text_input("Name")
    age = st.slider("Age", min_value=1, max_value=100)
    weight = st.slider("Weight (kg)", min_value=1, max_value=300)
    height = st.slider("Height (cm)", min_value=50, max_value=300)
    lifestyle = st.selectbox("Lifestyle", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    gender = st.selectbox("Gender", ["Male", "Female"])

    if st.button("Calculate"):
        # Create an instance of the Expert System
        expert_system = HealthExpert()
        # Insert user input as facts into the Expert System
        expert_system.reset()
        expert_system.declare(Name(name=name))
        expert_system.declare(Age(age=age))
        expert_system.declare(Weight(weight=weight))
        expert_system.declare(Height(height=height))
        expert_system.declare(Lifestyle(lifestyle=lifestyle))
        expert_system.declare(Gender(gender=gender))
        # Run the Expert System
        expert_system.run()


if __name__ == "__main__":
    main()
