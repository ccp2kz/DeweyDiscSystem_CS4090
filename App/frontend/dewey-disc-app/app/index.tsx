import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";

export default function HomeScreen() {
  const [distance, setDistance] = useState("");
  const [windSpeed, setWindSpeed] = useState("");
  const [recommendation, setRecommendation] = useState<string | null>(null);

  const getRecommendation = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: 1,
          distance_to_pin: parseFloat(distance),
          wind_speed: parseFloat(windSpeed),
          wind_direction: "N",
        }),
      });

      const data = await response.json();
      setRecommendation(data.recommended_disc);
    } catch (error) {
      console.error("Error fetching recommendation:", error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dewey Disc System</Text>

      <TextInput
        style={styles.input}
        placeholder="Distance to pin (ft)"
        value={distance}
        onChangeText={setDistance}
        keyboardType="numeric"
      />

      <TextInput
        style={styles.input}
        placeholder="Wind speed (mph)"
        value={windSpeed}
        onChangeText={setWindSpeed}
        keyboardType="numeric"
      />

      <Button title="Get Recommendation" onPress={getRecommendation} />

      {recommendation && (
        <Text style={styles.result}>Recommended Disc: {recommendation}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", padding: 20 },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 20 },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 10, width: "80%", marginBottom: 10 },
  result: { marginTop: 20, fontSize: 18 },
});

