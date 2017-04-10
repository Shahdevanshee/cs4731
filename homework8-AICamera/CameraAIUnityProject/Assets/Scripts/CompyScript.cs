using UnityEngine;
using System.Collections;

public class CompyScript : MonoBehaviour {
    public float maxWalkDistance;
    public float minWaitTime;
    public float maxWaitTime;

    private UnityEngine.AI.NavMeshAgent agent;
    private float curTime;
    private float timeToNextMove;
    private Vector3 targetPos;

	// Use this for initialization
	void Start () {
        agent = GetComponent<UnityEngine.AI.NavMeshAgent>();
        curTime = 0;
        timeToNextMove = Random.Range(minWaitTime, maxWaitTime);
	}
	
	// Update is called once per frame
	void Update () {
        if (curTime > timeToNextMove)
        {
            Vector3 randomDirection = Random.insideUnitSphere * maxWalkDistance;
            randomDirection += transform.position;
            UnityEngine.AI.NavMeshHit hit;
            UnityEngine.AI.NavMesh.SamplePosition(randomDirection, out hit, maxWalkDistance, 1);
            targetPos = hit.position;
            agent.SetDestination(targetPos);
            curTime = 0;
            timeToNextMove = Random.Range(minWaitTime, maxWaitTime);

        }
        curTime += Time.deltaTime;
	}
}
