package main

import (
	"log"
	"net/http"
)

func handleNewServers(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("error: could not upgrade websocket")
		return
	}
	session := Session{
		ws:  ws,
		SID: "noAuth",
	}
	defer ws.Close()
	for {
		if session.SID == "noAuth" {
			var authDetails ServerAuthRequest
			err = session.ws.ReadJSON(&authDetails)
			if err != nil {
				log.Printf("error: %v", err)
				session = Session{}
				break
			}
			if authDetails.AuthToken == "" || authDetails.ServiceID == "" || authDetails.UserID == "" {
				log.Printf("error: empty values for authentication provided")
				session = Session{}
				break
			}
			if !auth(authDetails.UserID, authDetails.AuthToken, authDetails.ServiceID) {
				log.Printf("error: hack attempt, failed authorization")
				session = Session{}
				break
			}
			session.SID = authDetails.ServiceID
		} else {
			var payload ServerPayload
			err = session.ws.ReadJSON(&payload)
			if err != nil {
				log.Printf("error: %v", err)
				session = Session{}
				break
			}
			if payload.ServiceID == "" {
				log.Printf("error: service id not provided, deleting")
				session = Session{}
				break
			}
			if payload.ServiceID != session.SID {
				log.Printf("error: unauthenticated request made, deleting")
				session = Session{}
				break
			}
			if !payload.Heartbeat {
				broadcast <- payload
			} else {
				err = session.ws.WriteJSON(HeartbeatMessage{Success: true})
				if err != nil {
					log.Printf("error: was unable to respond to heartbeat")
					session = Session{}
					break
				}
			}
		}
	}
}
