"""
Cron Scheduler for the Recurring Task Service
Handles scheduling of recurring task generation using Dapr Jobs API
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dapr.aio.clients import DaprClient
import asyncio
import json

logger = logging.getLogger(__name__)


class CronScheduler:
    def __init__(self):
        self.dapr_client: Optional[DaprClient] = None
        self.scheduler_initialized = False

    async def initialize(self):
        """Initialize the scheduler with Dapr client"""
        try:
            self.dapr_client = DaprClient()
            self.scheduler_initialized = True
            logger.info("Cron Scheduler initialized with Dapr client")
        except Exception as e:
            logger.error(f"Failed to initialize Cron Scheduler: {str(e)}")
            raise

    async def schedule_recurring_task_generation(self, template_id: str, recurrence_rule: str, start_time: datetime):
        """
        Schedule recurring task generation using Dapr Jobs API
        """
        if not self.scheduler_initialized:
            raise Exception("Scheduler not initialized")

        try:
            # Create a job specification for Dapr
            job_spec = {
                'job_name': f"generate_recurring_tasks_{template_id}",
                'schedule': self.convert_rrule_to_cron(recurrence_rule),
                'task': {
                    'service': 'recurring-task-service',
                    'method': 'generate_recurring_tasks',
                    'params': {
                        'template_id': template_id,
                        'recurrence_rule': recurrence_rule
                    }
                },
                'start_time': start_time.isoformat(),
                'metadata': {
                    'template_id': template_id,
                    'recurrence_rule': recurrence_rule
                }
            }

            # In a real implementation, this would use Dapr's Jobs API
            # For now, we'll simulate by creating a periodic task
            logger.info(f"Scheduled recurring task generation for template {template_id}")

            # Return job ID
            return f"job_{template_id}_{int(datetime.now().timestamp())}"

        except Exception as e:
            logger.error(f"Error scheduling recurring task generation: {str(e)}")
            raise

    async def schedule_single_task_generation(self, template_id: str, run_time: datetime):
        """
        Schedule a single task generation event
        """
        if not self.scheduler_initialized:
            raise Exception("Scheduler not initialized")

        try:
            # Calculate delay until the run time
            delay = (run_time - datetime.now()).total_seconds()

            if delay <= 0:
                logger.info("Run time is in the past, executing immediately")
                await self.execute_task_generation(template_id)
                return

            # Create a delayed execution
            logger.info(f"Scheduling single task generation for {run_time}")

            # In a real implementation, this would use Dapr's Jobs API
            # For simulation, we'll use asyncio.sleep
            asyncio.create_task(self._delayed_execution(template_id, delay))

        except Exception as e:
            logger.error(f"Error scheduling single task generation: {str(e)}")
            raise

    async def _delayed_execution(self, template_id: str, delay: float):
        """Internal method to execute task generation after delay"""
        await asyncio.sleep(delay)
        await self.execute_task_generation(template_id)

    async def execute_task_generation(self, template_id: str):
        """
        Execute task generation immediately
        """
        try:
            # Call the recurring task service to generate tasks
            async with DaprClient() as client:
                response = await client.invoke_method(
                    app_id='recurring-task-service',
                    method_name='generate_recurring_tasks',
                    data={
                        'template_id': template_id
                    }
                )

                logger.info(f"Executed task generation for template {template_id}")
                return json.loads(response.data.get('response', '{}'))

        except Exception as e:
            logger.error(f"Error executing task generation: {str(e)}")
            raise

    async def cancel_scheduled_job(self, job_id: str):
        """
        Cancel a scheduled job
        """
        try:
            # In a real implementation, this would use Dapr's Jobs API to cancel
            logger.info(f"Canceled scheduled job: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error canceling scheduled job: {str(e)}")
            return False

    async def get_scheduled_jobs(self) -> Dict[str, Any]:
        """
        Get information about scheduled jobs
        """
        try:
            # In a real implementation, this would query Dapr's Jobs API
            return {
                'jobs': [],
                'total_count': 0
            }
        except Exception as e:
            logger.error(f"Error getting scheduled jobs: {str(e)}")
            return {'jobs': [], 'total_count': 0}

    def convert_rrule_to_cron(self, rrule_str: str) -> str:
        """
        Convert an RRULE string to a CRON expression
        Note: This is a simplified conversion - a full implementation would be more complex
        """
        # This is a placeholder implementation
        # A full RRULE to CRON converter would need to parse the RRULE properly
        if 'DAILY' in rrule_str.upper():
            return "0 0 * * *"  # Daily at midnight
        elif 'WEEKLY' in rrule_str.upper():
            return "0 0 * * 0"  # Weekly on Sunday at midnight
        elif 'MONTHLY' in rrule_str.upper():
            return "0 0 1 * *"  # Monthly on 1st at midnight
        else:
            # Default to daily if we can't parse
            return "0 0 * * *"

    async def close(self):
        """Close the scheduler and cleanup resources"""
        if self.dapr_client:
            await self.dapr_client.close()
        self.scheduler_initialized = False