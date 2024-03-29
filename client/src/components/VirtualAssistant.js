import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function VirtualAssistant() {
	const [question, setQuestion] = useState("");
	const [messages, setMessages] = useState([]);
	const [isLoading, setIsLoading] = useState(false);
	const [threadId, setThreadId] = useState("");

	useEffect(() => {
		async function initThread() {
			try {
				const response = await axios.get(`http://localhost:8000/init_thread/`);
				setThreadId(response.data.thread_id);
			} catch (error) {
				console.error("Error initializing thread:", error);
			}
		}
		initThread();
	}, []);

	const handleSubmit = async () => {
		if (!question.trim()) return;
		setIsLoading(true);
		try {
			const response = await axios.get(`http://localhost:8000/ask/?question=${question}&thread_id=${threadId}`);
			const answer = response.data.answer;
			const newMessage = {
				role: "user",
				content: (
					<>
						<span style={{ fontWeight: "bold", color: "blue" }}>You:</span> {question}
					</>
				),
			};
			const botMessage = {
				role: "bot",
				content: (
					<>
						<span style={{ fontWeight: "bold", color: "red" }}>Gpt:</span> {answer}
					</>
				),
			};
			setMessages([...messages, newMessage, botMessage]);
		} catch (error) {
			console.error("Error fetching answer:", error);
			const errorMessage = { role: "bot", content: "Oops! Something went wrong. Please try again." };
			setMessages([...messages, errorMessage]);
		} finally {
			setIsLoading(false);
			setQuestion("");
		}
	};

	const handleKeyPress = (e) => {
		if (e.key === "Enter") {
			e.preventDefault();
			handleSubmit();
		}
	};

	return (
		<div className="container mt-5">
			<h1>AI lỏ</h1>
			<div className="message-container">
				{messages.map((message, index) => (
					<div key={index} className={`message ${message.role}`}>
						<p>{message.content}</p>
					</div>
				))}
			</div>
			<div className="input-group mb-3">
				<input type="text" className="form-control" placeholder="Enter your question" value={question} onChange={(e) => setQuestion(e.target.value)} onKeyPress={handleKeyPress} />
				<button type="submit" className="btn btn-primary mr-2" onClick={handleSubmit} disabled={isLoading}>
					{isLoading ? "Loading..." : "Ask"}
				</button>
			</div>
		</div>
	);
}

export default VirtualAssistant;
