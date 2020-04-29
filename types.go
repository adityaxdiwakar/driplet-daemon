package main

import "github.com/gorilla/websocket"

// Message struct
type Message struct {
	Email    string `json:"email"`
	Username string `json:"username"`
	Message  string `json:"message"`
}

// Session object with websocket and service ID
type Session struct {
	ws  *websocket.Conn
	SID string
	UID string
}

// ServerAuthRequest for when server authenticates
type ServerAuthRequest struct {
	AuthToken string `json:"auth_token"`
	UserID    string `json:"user_id"`
	ServiceID string `json:"service_id"`
}

// ServerPayload datatype for incoming log messages
type ServerPayload struct {
	Heartbeat bool   `json:"heartbeat"`
	ServiceID string `json:"service_id"`
	Log       string `json:"log"`
	UserID    string `json:"user_id"`
}

// HeartbeatMessage to be sent back in case of heartbeat
type HeartbeatMessage struct {
	Success bool `json:"success"`
}

// ClientResponse to be sent to client
type ClientResponse struct {
	ServiceID string `json:"service_id"`
	Log       string `json:"log"`
}

// APIServices struct from response
type APIServices []struct {
	MongoID struct {
		Oid string `json:"$oid"`
	} `json:"_id"`
	Name           string   `json:"name"`
	Description    string   `json:"description"`
	StartCommand   string   `json:"start_command"`
	StopCommand    string   `json:"stop_command"`
	RestartCommand string   `json:"restart_command"`
	StatusCommand  string   `json:"status_command"`
	LogCommand     string   `json:"log_command"`
	ID             string   `json:"id"`
	AssociatedTo   string   `json:"associated_to"`
	Logs           []string `json:"logs"`
}
