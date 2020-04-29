package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

func auth(userID string, authToken string, serviceID string) bool {
	authURL := fmt.Sprintf("http://backend.driplet.adi.wtf/endpoints/%s/services", userID)

	client := &http.Client{}
	req, _ := http.NewRequest("GET", authURL, nil)
	req.Header.Set("authorization", string(authToken))
	resp, err := client.Do(req)
	if err != nil {
		return false
	}

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return false
	}
	var responseServices APIServices

	err = json.Unmarshal(body, &responseServices)
	if err != nil {
		return false
	}

	for _, service := range responseServices {
		if service.ID == serviceID {
			return true
		}
	}
	return false
}
