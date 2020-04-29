package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var clients = make(map[string][]Session) // connected clients
var broadcast = make(chan ServerPayload) // hand-off

var upgrader = websocket.Upgrader{}

func main() {
	http.HandleFunc("/ws/server", handleNewServers)
	http.HandleFunc("/ws/client", handleNewClients)
	go handleMessages()
	log.Println("http server started on :8000")
	err := http.ListenAndServe(":8000", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

func handleMessages() {
	for {
		// Grab the next message from the broadcast channel
		msg := <-broadcast
		// Send it out to every client that is currently connected
		directedSessions := clients[msg.ServiceID]
		for _, session := range directedSessions {
			err := session.ws.WriteJSON(ClientResponse{
				ServiceID: msg.ServiceID,
				Log:       msg.Log,
			})
			if err != nil {
				log.Printf("error %v", err)
				session.ws.Close()
			}
		}
	}
}
