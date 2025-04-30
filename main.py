import boto3
import logging
import os

region = os.environ.get("AWS_REGION")
taskfamily = os.environ.get("TASK_FAMILY") 

logger = logging.getLogger(__name__)
client = boto3.client("ecs", region_name=region)

def deregister_task_definition(task_definition_arn):
    logger.info(f'Deregistering: {task_definition_arn}')
    try:
        client.deregister_task_definition(
            taskDefinition=task_definition_arn
        )
        logger.info(f'Successfully deregistered: {task_definition_arn}')
        #return response
    except Exception as e:
        logger.error(f'Error deregistering task definition {task_definition_arn}: {e}')
        return None


def delete_task_definition(task_definition_arn):
    logger.info(f'Deleting: {task_definition_arn}')
    try:
        client.delete_task_definitions(
            taskDefinitions=[task_definition_arn]
        )
        logger.info(f'Successfully deleted: {task_definition_arn}')
    except Exception as e:
        logger.error(f'Error deleting task definition {task_definition_arn}: {e}')
        return None

def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Task family: " + taskfamily)
    activetasks = client.list_task_definitions(
        familyPrefix=taskfamily,
        status="ACTIVE",
        sort="ASC",
        maxResults=100
    )

    logger.info("Deregistering active task definitions")
    for task_definition_arn in activetasks["taskDefinitionArns"]:
        deregister_task_definition(task_definition_arn)

    logger.info("Done deregistering active task definitions")

    logger.info("Starting deleting inactive task definitions")
    inactivetasks = client.list_task_definitions(
        familyPrefix=taskfamily,
        status="INACTIVE",
        sort="ASC",
        maxResults=100
    )

    logger.info("Deleting inactive task definitions")
    for task_definition_arn in inactivetasks["taskDefinitionArns"]:
        logger.debug("Deleting: "+task_definition_arn)
        delete_task_definition(task_definition_arn)

    logger.info("Done deleting inactive task definitions")

if __name__ == "__main__":
    main()
