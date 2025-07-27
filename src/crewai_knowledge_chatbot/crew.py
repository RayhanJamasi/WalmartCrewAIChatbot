from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

#specifications for the memory
memory_config = {
    "provider": "mem0",
    "config": {"user_id": "User"}
}

#creating a crew base class
@CrewBase
class CrewaiKnowledgeChatbot():
    """CrewaiKnowledgeChatbot crew"""

    #accessing the agent and yask YAML files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    #creating a researcher agent
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            #giving access to serper search tool, with searching for things in toronto ontario
            tools=[SerperDevTool(n_results=2,country="ca", locale="en-CA", location="Toronto, Ontario, Canada")], 
            memory=True, 
            memory_config=memory_config, 
            verbose=True,
            max_iter = 3
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            memory=False,
            verbose=True,
            max_iter = 2
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher()
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], 
            agent = self.reporting_analyst(),
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiKnowledgeChatbot crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=False,
            # process=Process.hierarchical, 
        )
