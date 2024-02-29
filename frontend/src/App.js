import React, {useEffect, useState} from "react";

// Used Material UI for creating the chat Interface
import {Box, Button, Card, CardContent, Grid, TextField} from "@mui/material";
//

// Created a saperate component for displaying the message cards
import Message from "./Message";

// for making the API request
import axios from "axios";

// Server URL
const baseURL = "http://127.0.0.1:5000";

function App() {

  const messagesListRef = React.createRef();
  const [messageInput, setMessageInput] = useState("");
  
  // Stores the history of all the messages
  const [messages, setMessages] = useState([]);

  useEffect(() => {

      setMessages([{content:"Hello !! Ask me anything on Pan :)", isCustomer:false}])
    // })
  }, []);

  const sendMessage = (content) => {
    setMessages([
      ...messages,
      {content: content,isCustomer: true}
    ]);

    // API call to the backend sending the query

    axios.get(baseURL+"?query="+content).then(res => {
      console.log(res);
      
      // Setting the response to the start variable to display it in the chat
      setMessages(prevState => [
        ...prevState,
        {content:res.data["answer"], isCustomer:false},
      ]);
    });
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    sendMessage(messageInput);
    setMessageInput("");
  }

  useEffect(() => {
    
    // to ensure that the chat scrolls to the recent chat in the card

    messagesListRef.current.scrollTop = messagesListRef.current.scrollHeight;
  }, [messagesListRef, messages]);

  return (
    <Grid
      container
      direction="row"
      justifyContent="right"
      alignItems="center"
      
    >
      <h2
        style={{marginRight:"42vw", position:"absolute", top:"1px", zIndex:"100"}}
      >
        Pan Card Support
      </h2>
      
      <Card sx={{height:"95vh", width:"100vw", backgroundColor:"#353441", position:"relative", top:"5vh"}}>
        <CardContent>
          <Box
            ref={messagesListRef}
            sx={{
              height:"80vh",
              overflow: "scroll",
              overflowX: "hidden",
            }}
          >
            {/* 
            
            Loops through the messages variable(stores all the chat history and displayes the Message component) 
            
            */}
            
            <Box sx={{m: 1, mr: 2}}>
              {messages && messages.map((message, index) =>{
                return(
                    <Message
                      key={index}
                      content={message.content}
                      isCustomer={message.isCustomer}
                  />
                )
              })}
            </Box>
          </Box>
          <Box
            component="form"
            sx={{
              mt: 2,
              display: "flex",
              flexFlow: "row",
              gap: 1,
              backgroundColor:"#41404f"
            }}
          >
            <TextField
              variant="outlined"
              size="small"
              placeholder="Ask me anything..."
              sx={{input:{color:"white"}}}
              value={messageInput}
              onChange={(event) => setMessageInput(event.target.value)}
              fullWidth
            />
            <Button
              variant="contained"
              onClick={handleSubmit}
              type="submit"
            >
              Send
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Grid>
  );
}

export default App;
