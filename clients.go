package main

import (
	"log"
	"net/http"
)

func handleNewClients(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("error: could not upgrade websocket: %v", err)
		return
	}
	defer ws.Close()
	session := Session{
		ws:  ws,
		SID: "noAuth",
		UID: "",
	}
	for {
		if session.SID == "noAuth" {
			var authDetails ServerAuthRequest
			err = session.ws.ReadJSON(&authDetails)
			if err != nil {
				log.Printf("error: %v", err)
				session = Session{}
				break
			}
			if !auth(authDetails.UserID, authDetails.AuthToken, authDetails.ServiceID) {
				log.Printf("error: hack attempt, failed authorization")
				session = Session{}
				break
			}
			session.SID = authDetails.ServiceID
			session.UID = authDetails.UserID
			clients[session.UID] = append(clients[session.UID], session)
		} else {
			var heartbeat HeartbeatMessage
			err = session.ws.ReadJSON(&heartbeat)
			if err != nil {
				log.Printf("error: %v", err)
				session = Session{}
				break
			}
			err = session.ws.WriteJSON(HeartbeatMessage{Success: true})
			if err != nil {
				log.Printf("error: was unable to respond to heartbeat")
				session = Session{}
				break
			}
		}
	}
}
