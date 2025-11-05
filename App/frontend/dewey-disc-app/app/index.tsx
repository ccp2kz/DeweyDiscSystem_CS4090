import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, StyleSheet, FlatList } from "react-native";


export default function Home() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState<string | null>(null);

  const [courses, setCourses] = useState<any[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<string | null>(null);

  const [distance, setDistance] = useState("");
  const [wind, setWind] = useState("");
  const [recommendation, setRecommendation] = useState<string | null>(null);

  const BASE_URL = "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${BASE_URL}/courses`)
      .then((res) => res.json())
      .then(setCourses)
      .catch(console.error);
  }, []);

  const register = async () => {
    const res = await fetch(`${BASE_URL}/register?username=${username}&email=${email}&password=${password}`, { method: "POST" });
    const data = await res.json();
    setUserId(data.user_id);
  };

  const getRecommendation = async () => {
    if (!userId || !selectedCourse) return alert("Select course and create account first!");
    const res = await fetch(`${BASE_URL}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        course_id: selectedCourse,
        distance_to_pin: parseFloat(distance),
        wind_speed: parseFloat(wind),
        wind_direction: "N",
      }),
    });
    const data = await res.json();
    setRecommendation(data.recommended_disc);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dewey Disc System</Text>

      {!userId && (
        <>
          <TextInput placeholder="Username" style={styles.input} value={username} onChangeText={setUsername} />
          <TextInput placeholder="Email" style={styles.input} value={email} onChangeText={setEmail} />
          <TextInput placeholder="Password" style={styles.input} secureTextEntry value={password} onChangeText={setPassword} />
          <Button title="Create Account" onPress={register} />
        </>
      )}

      {userId && (
        <>
          <Text style={styles.subtitle}>Select Course:</Text>
          <FlatList
            data={courses}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <Button
                title={item.name}
                onPress={() => setSelectedCourse(item.id)}
                color={selectedCourse === item.id ? "green" : "blue"}
              />
            )}
          />

          <TextInput
            placeholder="Distance to pin (ft)"
            style={styles.input}
            value={distance}
            onChangeText={setDistance}
            keyboardType="numeric"
          />
          <TextInput
            placeholder="Wind speed (mph)"
            style={styles.input}
            value={wind}
            onChangeText={setWind}
            keyboardType="numeric"
          />
          <Button title="Get Recommendation" onPress={getRecommendation} />
        </>
      )}

      {recommendation && <Text style={styles.result}>Recommended Disc: {recommendation}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10, textAlign: "center" },
  subtitle: { marginTop: 20, fontSize: 18, fontWeight: "bold" },
  input: { borderWidth: 1, borderColor: "#ccc", marginVertical: 5, padding: 8 },
  result: { marginTop: 20, fontSize: 18, textAlign: "center" },
});

